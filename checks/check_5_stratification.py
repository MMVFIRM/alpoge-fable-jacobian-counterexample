"""CHECK 5 (Paper I item 6): the constructible 3/1/0 fiber stratification.
  #F^{-1}(q) = 3 on C^3 \\ S_F   (CHECK 3 gives a generic instance; propriety
                                  off S_F makes the count constant)
             = 1 on S_F \\ Gamma
             = 0 on Gamma = {27AC^2-4 = 0, 3BC-4 = 0}
(a) Saturation gate: the ORIGINAL fiber equations over Gamma, with C
    inverted (Rabinowitsch), generate the unit ideal: no point of C^3 maps
    into Gamma. (Also immediate from M|_Gamma = -2C, but this check does not
    use M at all.)
(b) Explicit section on S_F\\Gamma: with x0 = 2v(v^2-a)/(v^2-3a)^2 and
    u0 = 4av^2/(v^2-3a)^2, F(x0,y0,z0) = (a, (v^2+3a)/v, (v^2-a)/v^3) as an
    exact identity in (v,a); denominators only v and (v^2-3a) [= Gamma].
(c) Exact fiber over (1,4,0) in S_F\\Gamma: exactly {(0,4,-63)}.
Requires: sympy. Runtime: 1-3 minutes ((a) Groebner + (c) solve)."""
import sympy as sp
x, y, z, t, v, a = sp.symbols('x y z t v a')
C = sp.Symbol('C')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
G = sp.groebner([sp.expand(27*C**2*F1 - 4), sp.expand(3*C*F2 - 4),
                 sp.expand(F3 - C), t*C - 1], x, y, z, C, t, order='grevlex')
assert list(G.exprs) == [1], "FAIL: saturation gate"
print("PASS (a): (I_Gamma : C^infty) = (1) -- fibers over Gamma are empty.")
Av, Bv, Cv = a, (v**2 + 3*a)/v, (v**2 - a)/v**3
x0 = sp.cancel(2*Cv/(4 - 3*Bv*Cv))
u0 = sp.cancel(4*a*v**2/(v**2 - 3*a)**2)
y0 = sp.cancel(Bv - 3*x0*Av/u0)
z0 = sp.cancel((Av/u0 - y0**2*(4 + 3*x0*y0))/u0**2)
chk = [sp.cancel(sp.expand(Fi.subs({x: x0, y: y0, z: z0})) - tv)
       for Fi, tv in [(F1, Av), (F2, Bv), (F3, Cv)]]
assert all(e == 0 for e in chk), "FAIL: section identity"
print("PASS (b): explicit section verifies on all of the chart minus Gamma.")
sols = sp.solve([F1 - 1, F2 - 4, F3], [x, y, z], dict=True)
assert sols == [{x: 0, y: 4, z: -63}], "FAIL: fiber over (1,4,0)"
print("PASS (c): fiber over (1,4,0) is exactly {(0,4,-63)}.")
print("PASS: stratification 3 / 1 / 0 on C^3\\S_F, S_F\\Gamma, Gamma certified.")
