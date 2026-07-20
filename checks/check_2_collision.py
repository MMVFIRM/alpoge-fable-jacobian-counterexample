"""CHECK 2 (Paper I item 3): three distinct points, one image — exactly.
Requires: sympy. Runtime: seconds. Independent of all other checks.
Together with CHECK 1 this falsifies the Jacobian Conjecture in dimension 3."""
import sympy as sp
x, y, z = sp.symbols('x y z')
s = x*y; u = 1 + s
F = (sp.expand(u**3*z + y**2*u*(4+3*s)),
     sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s)),
     sp.expand(2*x - 3*x**2*y - x**3*z))
P = [(0, 0, sp.Rational(-1, 4)),
     (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
     (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
assert len(set(P)) == 3, "FAIL: points not distinct"
images = [tuple(sp.simplify(Fi.subs({x: p[0], y: p[1], z: p[2]})) for Fi in F) for p in P]
for p, im in zip(P, images):
    print(f"F{p} = {im}")
target = (sp.Rational(-1, 4), 0, 0)
assert all(im == target for im in images), "FAIL: images differ"
print("PASS: three distinct points map to (-1/4, 0, 0); F is not injective.")
