"""
Dissecting the Alpoge-Fable Jacobian counterexample (posted 2026-07-19).

F(x,y,z) = ( u^3 z + y^2 u (4+3s),
             y + 3x u^2 z + 3x y^2 (4+3s),
             2x - 3x^2 y - x^3 z )        where s = xy, u = 1+s.

Sections:
  1. Hidden structure identities (verified symbolically, exact)
  2. Fiber machinery: eliminate to 2 eqs in (x,u); resultant -> generic fiber count
  3. Surjectivity: compute candidate missed values; verify EXACTLY via solve
  4. Parametric family: g(s)=a+bs, F3 = al x + be x^2 y + ga x^3 z;
     impose det J = const; solve; verify a new member as counterexample
"""
import sys, time, signal, traceback
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

x, y, z, U = sp.symbols('x y z U')
A, B, C = sp.symbols('A B C')
s = x*y
u = 1 + s

W  = sp.expand(u**2*z + y**2*(4+3*s))
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)

def alarm_run(fn, secs, default=None):
    def h(sig, frm): raise TimeoutError
    old = signal.signal(signal.SIGALRM, h)
    signal.alarm(secs)
    try:
        r = fn()
    except TimeoutError:
        r = default
    except Exception:
        traceback.print_exc()
        r = default
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
    return r

print("="*72)
print("1. STRUCTURE IDENTITIES (exact symbolic checks)")
print("="*72)
print("  F1 == u*W                    :", sp.expand(F1 - u*W) == 0)
print("  F2 == y + 3x*W               :", sp.expand(F2 - (y + 3*x*W)) == 0)
print("  u^2*F3 == x(2+s) - x^3*W     :", sp.expand(u**2*F3 - (x*(2+s) - x**3*W)) == 0)
print("  (so the whole map factors through the single 'potential' W)")

print()
print("="*72)
print("2. FIBER STRUCTURE / TOPOLOGICAL DEGREE")
print("="*72)
# On u != 0:  W = A/u ;  y = B - 3xA/u ;  u = 1+xy  =>
P1 = U**2 - U*(1 + x*B) + 3*x**2*A
# u^2 F3 = x(2+s) - x^3 W  with 2+s = 1+u  =>  (times u):
P2 = U**3*C - x*U*(1 + U) + x**3*A
R = sp.expand(sp.resultant(P1, P2, U))
Rp = sp.Poly(R, x)
print("  Resultant R(x; A,B,C): degree in x =", Rp.degree())

Fn = sp.lambdify((x, y, z), (F1, F2, F3), 'mpmath')

def preimages(Av, Bv, Cv, tol=1e-6):
    """All preimages of (Av,Bv,Cv), numerically, via the exact elimination."""
    Rs = sp.expand(R.subs({A: sp.nsimplify(Av), B: sp.nsimplify(Bv), C: sp.nsimplify(Cv)}))
    p = sp.Poly(Rs, x)
    if p.degree() <= 0:
        return [], p.degree()
    roots = p.nroots(n=35, maxsteps=300)
    found = {}
    Avc, Bvc, Cvc = [mp.mpc(v) for v in (Av, Bv, Cv)]
    for r0 in roots:
        x0 = mp.mpc(complex(r0))
        disc = mp.sqrt((1 + x0*Bvc)**2 - 12*x0**2*Avc)
        for U0 in [((1 + x0*Bvc) + disc)/2, ((1 + x0*Bvc) - disc)/2]:
            if abs(U0) < 1e-12:
                continue
            if abs(U0**3*Cvc - x0*U0*(1 + U0) + x0**3*Avc) > 1e-8*(1 + abs(U0)**3):
                continue
            y0 = Bvc - 3*x0*Avc/U0
            if abs(1 + x0*y0 - U0) > 1e-8:
                continue
            z0 = (Avc/U0 - y0**2*(4 + 3*x0*y0))/U0**2
            v = Fn(x0, y0, z0)
            err = max(abs(v[0]-Avc), abs(v[1]-Bvc), abs(v[2]-Cvc))
            if err < tol:
                key = (round(float(x0.real), 6), round(float(x0.imag), 6),
                       round(float(y0.real), 6), round(float(y0.imag), 6),
                       round(float(z0.real), 6), round(float(z0.imag), 6))
                found[key] = (x0, y0, z0, err)
    return list(found.values()), p.degree()

targets = [
    (sp.Rational(2,3), sp.Rational(1,5), sp.Rational(-3,7)),
    (-1, 2, sp.Rational(1,2)),
    (5, sp.Rational(-1,3), 4),
    (sp.Rational(1,9), 7, -2),
    (sp.Rational(-4,5), -6, 9),
]
counts = []
for (Av, Bv, Cv) in targets:
    pts, degx = preimages(float(Av), float(Bv), float(Cv))
    counts.append(len(pts))
    print(f"  target ({Av},{Bv},{Cv}): deg_x R = {degx}, verified preimages = {len(pts)}")
print("  GENERIC FIBER SIZE (empirical):", counts)

# special point sanity: should recover exactly the 3 known preimages
pts, _ = preimages(-0.25, 0.0, 0.0)
print(f"  special point (-1/4,0,0): verified preimages = {len(pts)} (known: 3)")

# cross-validate one target exactly with Groebner (may be slow)
def exact_count():
    sols = sp.solve([F1 - sp.Rational(2,3), F2 - sp.Rational(1,5), F3 + sp.Rational(3,7)],
                    [x, y, z], dict=True)
    return len(sols)
n_exact = alarm_run(exact_count, 120)
print("  exact Groebner cross-check for target 1:", n_exact if n_exact is not None else "timeout (resultant count stands)")

print()
print("="*72)
print("3. SURJECTIVITY: does the map miss anything?")
print("="*72)
coeffs = Rp.all_coeffs()   # leading first, constant last
conds = [sp.expand(c) for c in coeffs[:-1]]
def missed():
    return sp.solve(conds, [A, B, C], dict=True)
msols = alarm_run(missed, 120, default=None)
print("  values where R(x) degenerates to a constant:", msols)
if msols:
    for msol in msols:
        const = sp.simplify(coeffs[-1].subs(msol))
        print("   -> R constant value there:", const, "(nonzero => candidate missed values)")
# EXACT ground-truth check of a candidate missed value:
def exact_empty(A0, B0, C0):
    return sp.solve([F1 - A0, F2 - B0, F3 - C0], [x, y, z], dict=True)
for cand in [(0, 0, 1), (0, 1, 1), (0, sp.Rational(1,2), -3)]:
    r = alarm_run(lambda c=cand: exact_empty(*c), 90, default="timeout")
    print(f"  exact solve F = {cand}: {'EMPTY - point NOT in image' if r == [] else r if r=='timeout' else f'{len(r)} preimage(s): {r}'}")
# and a nearby control point that SHOULD be hit:
r = alarm_run(lambda: exact_empty(sp.Rational(1,100), 0, 1), 90, default="timeout")
print("  control F = (1/100,0,1):", "timeout" if r == "timeout" else f"{len(r)} preimage(s) -> in image")

print()
print("="*72)
print("4. PARAMETRIC FAMILY:  g(s)=a+bs,  F3 = al*x + be*x^2 y + ga*x^3 z")
print("="*72)
a, b, al, be, ga = sp.symbols('a b alpha beta gamma')
g   = a + b*s
Wg  = sp.expand(u**2*z + y**2*g)
F1g = sp.expand(u*Wg)
F2g = sp.expand(y + 3*x*Wg)
F3g = al*x + be*x**2*y + ga*x**3*z
D = sp.expand(sp.Matrix([F1g, F2g, F3g]).jacobian(sp.Matrix([x, y, z])).det())
pol = sp.Poly(D, x, y, z)
eqs, const_term = [], sp.Integer(0)
for mono, c in zip(pol.monoms(), pol.coeffs()):
    if mono == (0, 0, 0):
        const_term = c
    else:
        eqs.append(sp.expand(c))
eqs = [e for e in set(eqs) if e != 0]
print("  # coefficient equations:", len(eqs))
fam = alarm_run(lambda: sp.solve(eqs, [a, b, al, be, ga], dict=True), 180, default=None)
print("  solutions (det J = const):")
if fam:
    for so in fam:
        det_val = sp.simplify(const_term.subs(so))
        print(f"    {so}   det = {det_val}")
    # pick a NON-original member with nonzero det and free parameters if any
    print()
    print("  --- verifying a NEW family member as a counterexample ---")
    # choose from the family: try substituting free params with fresh values
    chosen = None
    for so in fam:
        trial = dict(so)
        free = set()
        for v in trial.values():
            free |= getattr(v, 'free_symbols', set())
        full = dict(trial)
        # set any free symbols to a non-original value
        for fs in free | ({a, b, al, be, ga} - set(trial.keys())):
            full[fs] = sp.Integer(7) if fs == a else sp.Integer(5)
        vals = {k: sp.sympify(vv).subs(full) for k, vv in trial.items()}
        vals.update({k: v for k, v in full.items() if k in (a, b, al, be, ga) and k not in vals})
        dv = sp.simplify(const_term.subs(vals))
        # skip the exact original coefficients
        orig = {a: 4, b: 3, al: 2, be: -3, ga: -1}
        if dv != 0 and any(sp.simplify(vals.get(k, orig[k]) - orig[k]) != 0 for k in orig):
            chosen = vals
            break
    if chosen:
        print("    chosen coefficients:", {str(k): v for k, v in chosen.items()})
        F1c = F1g.subs(chosen); F2c = F2g.subs(chosen); F3c = F3g.subs(chosen)
        from conjecture_tester import ConjectureTester
        T = ConjectureTester()
        const_ok, dvv = T.is_constant_nonzero_jacobian([F1c, F2c, F3c], [x, y, z])
        print("    det J =", dvv, "| constant nonzero:", const_ok)
        # fiber count via generalized elimination:
        av, bv = chosen.get(a), chosen.get(b)
        alv, bev, gav = chosen.get(al), chosen.get(be), chosen.get(ga)
        P2g = U**3*C - x*(alv*U**3 + bev*(U-1)*U**3 + gav*x**2*A
                          - gav*U*(U-1)**2*(av + bv*(U-1)))
        Rg = sp.expand(sp.resultant(P1, P2g, U))
        Fcn = sp.lambdify((x, y, z), (F1c, F2c, F3c), 'mpmath')
        def preimages_g(Av, Bv, Cv, tol=1e-6):
            Rs = sp.expand(Rg.subs({A: sp.nsimplify(Av), B: sp.nsimplify(Bv), C: sp.nsimplify(Cv)}))
            p = sp.Poly(Rs, x)
            if p.degree() <= 0:
                return []
            roots = p.nroots(n=35, maxsteps=300)
            found = {}
            Avc, Bvc, Cvc = [mp.mpc(v) for v in (Av, Bv, Cv)]
            for r0 in roots:
                x0 = mp.mpc(complex(r0))
                disc = mp.sqrt((1 + x0*Bvc)**2 - 12*x0**2*Avc)
                for U0 in [((1 + x0*Bvc) + disc)/2, ((1 + x0*Bvc) - disc)/2]:
                    if abs(U0) < 1e-12:
                        continue
                    y0 = Bvc - 3*x0*Avc/U0
                    if abs(1 + x0*y0 - U0) > 1e-8:
                        continue
                    z0 = (Avc/U0 - y0**2*(float(av) + float(bv)*x0*y0))/U0**2
                    v = Fcn(x0, y0, z0)
                    err = max(abs(v[0]-Avc), abs(v[1]-Bvc), abs(v[2]-Cvc))
                    if err < tol:
                        key = tuple(round(float(t), 6) for t in
                                    (x0.real, x0.imag, y0.real, y0.imag, z0.real, z0.imag))
                        found[key] = (x0, y0, z0, err)
            return list(found.values())
        pts = preimages_g(0.37, -0.61, 0.83)
        print(f"    preimages of a random target: {len(pts)}")
        for (x0, y0, z0, err) in pts[:4]:
            print(f"      ({complex(x0):.6g}, {complex(y0):.6g}, {complex(z0):.6g})  |F-target| ~ {float(err):.1e}")
        if const_ok and len(pts) >= 2:
            print("    ==> NEW VERIFIED COUNTEREXAMPLE MEMBER (const nonzero Jacobian, non-injective)")
    else:
        print("    (no non-original member with nonzero det found in this ansatz)")
else:
    print("    solve timed out or returned nothing")
