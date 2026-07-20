"""
The Jelonek set (non-properness locus) and Galois structure of the
Alpoge-Fable counterexample F : C^3 -> C^3.

Derivation encoded here (hand analysis, machine-verified below):
Escapes to infinity with bounded image: take x -> oo, y -> v != 0 finite.
Then u ~ xv, W ~ A/u, and the limits force
    B = v + 3A/v          (from F2 = y + 3xW)
    C = (4v - B)/(3v^2)   (from u^2 F3 = x(1+u) - x^3 W at leading order)
Eliminating v gives the non-properness hypersurface S_F.

Sections:
  1. S_F exactly (resultant), sanity checks vs known fiber-drop curves
  2. Factor the fiber resultant R(x;A,B,C): valid cubic M vs spurious factor
  3. Galois test: is disc_x(M) a square in C(A,B,C)?  (S3 vs Z/3)
  4. Exact fiber over a generic point OF S_F  (expect: 1, not 3)
  5. Numeric monodromy permutation around S_F  (expect: transposition)
  6. Singular locus of S_F
"""
import sys, time, signal, traceback
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

x, y, z, U, v = sp.symbols('x y z U v')
A, B, C = sp.symbols('A B C')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)

def alarm_run(fn, secs, default=None):
    def h(sig, frm): raise TimeoutError
    old = signal.signal(signal.SIGALRM, h); signal.alarm(secs)
    try:
        r = fn()
    except TimeoutError:
        r = default
    except Exception:
        traceback.print_exc(); r = default
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM, old)
    return r

print("="*72)
print("1. THE JELONEK SET S_F (exact)")
print("="*72)
f1 = v**2 - B*v + 3*A          # v-relation from B = v + 3A/v
f2 = 3*C*v**2 - 4*v + B        # v-relation from C = (4v-B)/(3v^2)
S = sp.expand(sp.resultant(f1, f2, v))
print("  S_F equation:", sp.factor(S), "= 0")
Bp = v + 3*A/v
Cp = (4*v - Bp)/(3*v**2)
print("  parametrization check S(A,B(v),C(v)) == 0 :",
      sp.simplify(S.subs({B: Bp, C: Cp})) == 0)
print("  S on {A=0}:", sp.factor(S.subs(A, 0)),
      "  (fiber-drop curves found earlier: {B=0}, {BC=1})")
print("  S at the collision point (-1/4,0,0):",
      S.subs({A: -sp.Rational(1,4), B: 0, C: 0}), " (nonzero => NOT in S_F, consistent with its full 3-point fiber)")
print("  S is rational (parametrized by (A,v)) => uniruled, as Jelonek's theorem requires")

print()
print("="*72)
print("2. FIBER RESULTANT FACTORIZATION")
print("="*72)
P1 = U**2 - U*(1 + x*B) + 3*x**2*A
P2 = U**3*C - x*U*(1 + U) + x**3*A
R = sp.expand(sp.resultant(P1, P2, U))
fac = sp.factor(R)
print("  R factors as:")
print("   ", fac)
# identify the valid cubic (containing the true fiber x-coords) numerically
factors = [f for f, m in sp.factor_list(R)[1] if sp.degree(f, x) > 0]
tA, tB, tC = sp.Rational(2,3), sp.Rational(1,5), sp.Rational(-3,7)
# true preimage x-coords via direct exact solve (alarm-guarded)
def true_xs():
    sols = sp.solve([F1 - tA, F2 - tB, F3 - tC], [x, y, z], dict=True)
    return [sp.nsimplify(so[x], rational=False) for so in sols]
txs = alarm_run(true_xs, 150)
M = None
if txs:
    print(f"  true fiber x-coords over ({tA},{tB},{tC}): {len(txs)} points")
    for f in factors:
        fv = f.subs({A: tA, B: tB, C: tC})
        vals = [complex(sp.N(fv.subs(x, xx))) for xx in txs]
        if all(abs(vv) < 1e-18 for vv in vals):
            M = f
    print("  valid factor M(x;A,B,C) containing the fiber:", M)
else:
    print("  exact solve timed out; using degree heuristic")
    M = min(factors, key=lambda f: sp.degree(f, x))

print()
print("="*72)
print("3. GALOIS STRUCTURE: disc_x(M) a square in C(A,B,C)?")
print("="*72)
if M is not None:
    D = sp.discriminant(sp.Poly(M, x))
    Dfac = sp.factor(D)
    print("  disc_x(M) =", Dfac)
    # square iff every irreducible factor has even exponent
    _, flist = sp.factor_list(D)
    odd = [(f, m) for f, m in flist if m % 2 == 1]
    print("  factors with ODD exponent:", [(str(f), m) for f, m in odd] if odd else "none")
    if odd:
        print("  => disc is NOT a square  =>  Galois group = S3 (full symmetric)")
        print("  => the 3:1 cover is NOT cyclic/Galois; Galois closure is 6:1")
        # relation between disc locus and S_F:
        for f, m in odd:
            q = sp.simplify(sp.factor(f) / sp.factor(S))
            if q.is_number:
                print(f"  odd-exponent factor equals S_F equation (ratio {q}):")
                print("     => the Galois closure branches exactly over the Jelonek set")
    else:
        print("  => disc IS a square  =>  Galois group = Z/3 (cyclic cover)")

print()
print("="*72)
print("4. EXACT FIBER OVER A GENERIC POINT OF S_F")
print("="*72)
# (1,4,0) is on S_F  (v=1, A=1 => B=4, C=0). Hand-derivation predicts the
# unique preimage (0, 4, -63). Verify exactly:
print("  S(1,4,0) =", S.subs({A:1, B:4, C:0}), " (on S_F)")
def fiber_140():
    return sp.solve([F1 - 1, F2 - 4, F3 - 0], [x, y, z], dict=True)
r = alarm_run(fiber_140, 150, default="timeout")
print("  exact fiber over (1,4,0):", r)
print("  F(0,4,-63) =", (F1.subs({x:0,y:4,z:-63}), F2.subs({x:0,y:4,z:-63}), F3.subs({x:0,y:4,z:-63})))
# control just off S_F:
def fiber_off():
    return sp.solve([F1 - 1, F2 - 4, F3 - sp.Rational(1,10)], [x, y, z], dict=True)
r2 = alarm_run(fiber_off, 150, default="timeout")
print("  control fiber over (1,4,1/10) (off S_F):",
      "timeout" if r2 == "timeout" else f"{len(r2)} points")
# another on-surface sample, numeric, via M:
if M is not None:
    for (vv, aa) in [(2, 1), (sp.Rational(1,2), -1)]:
        bb = sp.simplify(Bp.subs({v: vv, A: aa}))
        cc = sp.simplify(Cp.subs({v: vv, A: aa}))
        Msub = sp.Poly(M.subs({A: aa, B: bb, C: cc}), x)
        print(f"  on-surface (A,B,C)=({aa},{bb},{cc}): valid cubic degenerates to degree {Msub.degree()}")

print()
print("="*72)
print("5. NUMERIC MONODROMY AROUND S_F")
print("="*72)
# base loop: (B,C)=(4,0) fixed, A = 1 + rho*exp(i theta).  S(A,4,0) is linear
# in A with the single zero A=1, so the loop encircles S_F exactly once.
print("  S(A,4,0) =", sp.factor(S.subs({B:4, C:0})), " -> single crossing at A=1")
if M is not None:
    import numpy as np
    Mnum = sp.lambdify((x, A, B, C), M, 'numpy')
    Mpoly_in_x = sp.Poly(M, x)
    coeff_funcs = [sp.lambdify((A, B, C), c, 'numpy') for c in Mpoly_in_x.all_coeffs()]
    def roots_at(Ax, Bx, Cx):
        cs = [f(Ax, Bx, Cx) for f in coeff_funcs]
        return np.roots(cs)
    rho, N = 0.7, 400
    Bx, Cx = 4.0, 0.0
    A0 = 1 + rho
    cur = list(roots_at(A0, Bx, Cx))
    start = list(cur)
    import itertools as it
    perm_track = list(range(len(cur)))
    for k in range(1, N+1):
        th = 2*np.pi*k/N
        Ax = 1 + rho*np.exp(1j*th)
        new = list(roots_at(Ax, Bx, Cx))
        # match new roots to cur by nearest
        best, bestd = None, None
        for pm in it.permutations(range(len(new))):
            d = sum(abs(new[pm[i]] - cur[i]) for i in range(len(cur)))
            if bestd is None or d < bestd:
                best, bestd = pm, d
        cur = [new[best[i]] for i in range(len(cur))]
    # final matching to start
    best, bestd = None, None
    for pm in it.permutations(range(len(start))):
        d = sum(abs(cur[i] - start[pm[i]]) for i in range(len(start)))
        if bestd is None or d < bestd:
            best, bestd = pm, d
    print(f"  loop A = 1 + {rho}e^(i th), {N} steps; root permutation (index i -> {list(best)})")
    cyc = "identity"
    if best != tuple(range(len(start))):
        moved = [i for i in range(len(start)) if best[i] != i]
        cyc = f"nontrivial, moves sheets {moved}"
    print("  monodromy:", cyc)
    print("  start roots:", [f"{r:.4f}" for r in start])
    print("  end   roots:", [f"{r:.4f}" for r in cur])

print()
print("="*72)
print("6. SINGULAR LOCUS OF S_F")
print("="*72)
grad = [sp.diff(S, w) for w in (A, B, C)]
def sing():
    return sp.solve([S] + grad, [A, B, C], dict=True)
sng = alarm_run(sing, 120, default="timeout")
print("  Sing(S_F):", sng)
