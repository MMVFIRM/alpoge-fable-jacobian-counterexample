"""CHECK 1 (Paper I items 1-2): the map and det J_F = -2, exactly.
Requires: sympy. Runtime: seconds. Independent of all other checks."""
import sympy as sp
x, y, z = sp.symbols('x y z')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
print("F1 =", F1); print("F2 =", F2); print("F3 =", F3)
d = sp.expand(sp.Matrix([F1, F2, F3]).jacobian(sp.Matrix([x, y, z])).det())
print("det J_F =", d)
assert d == -2, "FAIL: determinant is not the constant -2"
print("PASS: det J_F = -2 identically (F is a Keller map).")
