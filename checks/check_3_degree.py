"""CHECK 3 (Paper I item 4): generic degree 3.
(a) Master identity: M(x; F1,F2,F3) == 0 in C[x,y,z], where
    M = St*x^3 + (4-3BC)x - 2C, St = 27A^2C^2-18ABC+16A+B^3C-B^2.
    M(.;q) is never the zero polynomial (C=0 forces 4-3BC=4), so every
    preimage x-coordinate is a root of M(.;q): all fibers have <= 3 points.
(b) M is irreducible in Q[x,A,B,C] with coefficient content 1, hence
    irreducible over C(A,B,C) (Gauss).
(c) Exact Groebner fiber over the rational point (2/3, 1/5, -3/7): 3 points.
Requires: sympy. Runtime: (c) may take 1-3 minutes. Independent check."""
import sympy as sp
x, y, z, A, B, C = sp.symbols('x y z A B C')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
St = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
M = St*x**3 + (4 - 3*B*C)*x - 2*C
ident = sp.expand(M.subs({A: F1, B: F2, C: F3}))
assert ident == 0, "FAIL: master identity"
print("PASS (a): M(x; F(x,y,z)) == 0 identically.")
cont, fl = sp.factor_list(M)
assert len(fl) == 1 and fl[0][1] == 1 and cont == 1, "FAIL: M reducible"
assert sp.gcd(sp.gcd(St, 4 - 3*B*C), -2*C) == 1, "FAIL: content"
print("PASS (b): M irreducible over C(A,B,C); degree of x over the base is 3.")
sols = sp.solve([F1 - sp.Rational(2, 3), F2 - sp.Rational(1, 5),
                 F3 + sp.Rational(3, 7)], [x, y, z], dict=True)
print(f"exact fiber over (2/3, 1/5, -3/7): {len(sols)} points")
assert len(sols) == 3, "FAIL: fiber count"
print("PASS (c): generic degree = 3 (= field-extension degree, char 0).")
