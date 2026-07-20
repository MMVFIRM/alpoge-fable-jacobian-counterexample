"""CHECK 6 (Paper I item 7): S_3 structure and transposition monodromy.
(a) Res_U(P1, P2) = A * x^3 * M: the fiber cubic M emerges from elimination
    (P1, P2 encode the fiber equations in (x, U=1+xy) for u != 0).
(b) disc_x(M) = -4 * H^2 * St with H = 27AC^2 - 9BC + 8: the squarefree part
    contains St to the FIRST power => disc is not a square in C(A,B,C)
    => the Galois group of the degree-3 extension is the full S_3 (not Z/3).
(c) Res_A(St, H) = 27C^2(3BC-4)^3 and H|_{C=0} = 8: H meets S_F only in
    Gamma, so disc vanishes to odd order 1 across generic S_F: a meridian
    loop reverses sqrt(disc) => the meridian is an odd permutation, i.e. a
    TRANSPOSITION (exact parity argument, no numerics).
(d) Exact fiber at (-8/27, 0, 1) on {H=0}\\S_F: THREE distinct points, two
    sharing x = 3/4: the H^2 factor is an x-projection artifact, not
    branching (F is etale everywhere by CHECK 1).
Requires: sympy. Runtime: ~1 minute. Independent check."""
import sympy as sp
x, y, z, U, A, B, C = sp.symbols('x y z U A B C')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
St = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
M = St*x**3 + (4 - 3*B*C)*x - 2*C
H = 27*A*C**2 - 9*B*C + 8
P1 = U**2 - U*(1 + x*B) + 3*x**2*A
P2 = U**3*C - x*U*(1 + U) + x**3*A
R = sp.expand(sp.resultant(P1, P2, U))
assert sp.expand(R - A*x**3*M) == 0, "FAIL: resultant factorization"
print("PASS (a): Res_U(P1,P2) = A * x^3 * M.")
D = sp.discriminant(sp.Poly(M, x))
assert sp.expand(D + 4*H**2*St) == 0, "FAIL: discriminant identity"
_, fl = sp.factor_list(D)
odd = [f for f, m in fl if m % 2 == 1 and f.free_symbols]
assert len(odd) == 1 and sp.expand(odd[0] - St) == 0 or \
       (len(odd) == 1 and sp.simplify(odd[0]/St).is_number), "FAIL: parity"
print("PASS (b): disc_x(M) = -4 H^2 St, not a square: Galois group = S_3.")
RA = sp.factor(sp.resultant(St, H, A))
assert sp.expand(RA - 27*C**2*(3*B*C - 4)**3) == 0, "FAIL: H cap S_F"
assert H.subs(C, 0) == 8, "FAIL: H at C=0"
print("PASS (c): H ∩ S_F = Gamma; disc order 1 across S_F: meridian = transposition.")
pt = {A: sp.Rational(-8, 27), B: 0, C: 1}
assert sp.simplify(St.subs(pt)) != 0 and sp.simplify(H.subs(pt)) == 0
sols = sp.solve([F1 - pt[A], F2 - pt[B], F3 - pt[C]], [x, y, z], dict=True)
xs = sorted([so[x] for so in sols], key=str)
assert len(sols) == 3 and sorted([str(t) for t in xs]) == ['-3/2', '3/4', '3/4'], \
    f"FAIL: H-fiber structure: {xs}"
print("PASS (d): 3 distinct preimages at an H-point, two sharing x: no branching off S_F.")
