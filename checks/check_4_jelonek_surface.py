"""CHECK 4 (Paper I item 5): the exact Jelonek (non-properness) surface.
S_F : St = 27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0.
(a) St = (1/3)*Res_v(v^2 - Bv + 3A, 3Cv^2 - 4v + B): elimination of the
    escape direction v (escaping sheets satisfy y -> v, u ~ vx).
(b) Rational parametrization: St(a, (v^2+3a)/v, (v^2-a)/v^3) == 0
    (S_F is uniruled, as Jelonek's theorem requires).
(c) Square identity: 27C^2 * St|_{B=4/(3C)} = (27AC^2 - 4)^2, so
    S_F meets {4-3BC=0} exactly in Gamma = {27AC^2=4, 3BC=4}.
(d) St|_{A=0} = B^2(BC-1): the fiber-drop curves in the plane {A=0}.
(e) The collision point (-1/4,0,0) is NOT on S_F (St = -4 there).
Requires: sympy. Runtime: seconds. Independent check."""
import sympy as sp
A, B, C, v, a = sp.symbols('A B C v a')
St = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
R = sp.expand(sp.resultant(v**2 - B*v + 3*A, 3*C*v**2 - 4*v + B, v))
assert sp.expand(R - 3*St) == 0, "FAIL: resultant"
print("PASS (a): Res_v = 3*St.")
Bp, Cp = (v**2 + 3*a)/v, (v**2 - a)/v**3
assert sp.simplify(St.subs({A: a, B: Bp, C: Cp})) == 0, "FAIL: parametrization"
print("PASS (b): S_F rationally parametrized (uniruled).")
sq = sp.factor(sp.expand(27*C**2*St.subs(B, 4/(3*C))))
assert sp.expand(sq - (27*A*C**2 - 4)**2) == 0, "FAIL: square identity"
print("PASS (c): 27C^2*St|_{B=4/(3C)} = (27AC^2-4)^2.")
assert sp.factor(St.subs(A, 0)) == sp.factor(B**2*(B*C - 1)), "FAIL: A=0 slice"
print("PASS (d): St|_{A=0} = B^2(BC-1).")
assert St.subs({A: sp.Rational(-1, 4), B: 0, C: 0}) == -4, "FAIL: collision point"
print("PASS (e): the collision point is off S_F (its fiber is a generic one).")
