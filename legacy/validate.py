import sys, time
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp
from conjecture_tester import ConjectureTester

T = ConjectureTester()
x, y, z = sp.symbols('x y z')

print("="*70)
print("A. Identity checks (incl. the case GeoVerify got WRONG)")
print("="*70)
# GeoVerify called these two NON-equivalent at 0.85 conf. Truth: equal.
print("  x^3 - x  vs  x(x-1)(x+1):")
print("   ", T.prove_or_refute_identity(x**3 - x, x*(x-1)*(x+1)))
# A genuine non-identity, real-positive sampling would ALSO catch, but test complex-only case:
print("  sqrt(x^2)  vs  x   (equal on R+, NOT as functions on C):")
print("   ", T.prove_or_refute_identity(sp.sqrt(x**2), x))
# True identity needing complex sampling
print("  (x+I)(x-I)  vs  x^2+1:")
print("   ", T.prove_or_refute_identity((x+sp.I)*(x-sp.I), x**2+1))

print()
print("="*70)
print("B. Re-verify the Jacobian counterexample THROUGH the tool")
print("="*70)
F = [
    (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y),
    y + 3*x*(1 + x*y)**2 * z + 3*x*y**2*(4 + 3*x*y),
    2*x - 3*x**2*y - x**3*z,
]
pts = [(0, 0, sp.Rational(-1,4)),
       (1, sp.Rational(-3,2), sp.Rational(13,2)),
       (-1, sp.Rational(3,2), sp.Rational(13,2))]
v = T.test_jacobian_counterexample(F, [x, y, z], pts)
print("  jacobian det:", T.jacobian_det(F, [x,y,z]))
print("  verdict:", v)
print("  witness:", v.witness)

print()
print("="*70)
print("C. Rediscover a REAL counterexample by search:")
print("   Euler's sum-of-powers conjecture, n=5  (Euler: need >=5 fifth powers)")
print("   Search for a^5+b^5+c^5+d^5 = e^5  (only FOUR terms)")
print("="*70)
t0 = time.time()
LIMIT = 150
# Precompute fifth powers and a reverse lookup for perfect fifth powers
fifth = {i**5: i for i in range(1, LIMIT+1)}
fifth_set = set(fifth)
found = None
# iterate a<=b<=c<=d, test if the sum is a perfect fifth power
for a in range(1, LIMIT):
    a5 = a**5
    for b in range(a, LIMIT):
        b5 = b**5
        for c in range(b, LIMIT):
            c5 = c**5
            for d in range(c, LIMIT):
                s = a5 + b5 + c5 + d**5
                if s in fifth_set:
                    found = (a, b, c, d, fifth[s])
                    break
            if found: break
        if found: break
    if found: break
dt = time.time() - t0
if found:
    a,b,c,d,e = found
    # verify with the tester's exact Diophantine checker
    lhs = a**5+b**5+c**5+d**5
    e_check = T.is_perfect_power(lhs, 5)
    print(f"  COUNTEREXAMPLE FOUND in {dt:.1f}s: {a}^5 + {b}^5 + {c}^5 + {d}^5 = {e}^5")
    print(f"  tool re-check: {a}^5+{b}^5+{c}^5+{d}^5 = {lhs}, which is {e_check}^5  -> {e_check**5==lhs}")
else:
    print(f"  none found up to {LIMIT} in {dt:.1f}s")
