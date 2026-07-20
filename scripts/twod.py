"""
Does the u*W mechanism transfer to dimension 2?

3D counterexample structure: F = (uW, y+3xW, F3) with u=1+xy and a single
"potential" W. The natural 2D analogue is
    F = ( u*W(x,y),  y + lam*x*W(x,y) ),   u = 1+xy,
which is a local-diffeo counterexample in C^2 iff det J = nonzero constant
and W makes the map non-injective (W nonconstant).

We test ALL polynomial W of total degree <= DMAX, lam free, exactly:
expand det J, force every nonconstant coefficient to zero, solve.

Context (honest): the 2D Jacobian Conjecture is verified for degree <= ~100
(Moh 1983; pushed to 108 in 2022), so ANY 2D counterexample needs degree >100.
This probe cannot find one; it answers the sharper structural question of
whether THIS mechanism has a low-degree 2D analogue at all.
"""
import sys, time, signal, itertools
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp

x, y = sp.symbols('x y')
u = 1 + x*y
lam = sp.Symbol('lam')

def probe(DMAX, timeout=240):
    cs = {}
    W = sp.Integer(0)
    for i in range(DMAX+1):
        for j in range(DMAX+1-i):
            c = sp.Symbol(f'c{i}{j}')
            cs[(i, j)] = c
            W += c * x**i * y**j
    F1 = sp.expand(u*W)
    F2 = sp.expand(y + lam*x*W)
    D = sp.expand(sp.Matrix([F1, F2]).jacobian(sp.Matrix([x, y])).det())
    pol = sp.Poly(D, x, y)
    eqs, const = [], sp.Integer(0)
    for mono, c in zip(pol.monoms(), pol.coeffs()):
        if mono == (0, 0):
            const = c
        else:
            eqs.append(sp.expand(c))
    eqs = [e for e in set(eqs) if e != 0]
    unknowns = list(cs.values()) + [lam]
    print(f"  DMAX={DMAX}: {len(cs)} W-coefficients, {len(eqs)} equations")
    def run():
        return sp.solve(eqs, unknowns, dict=True)
    def h(sig, frm): raise TimeoutError
    old = signal.signal(signal.SIGALRM, h); signal.alarm(timeout)
    try:
        sols = run()
    except TimeoutError:
        print("   solve TIMED OUT"); return
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM, old)
    print(f"   solution branches: {len(sols)}")
    interesting = 0
    for so in sols:
        Wv = sp.expand(W.subs(so))
        dv = sp.simplify(const.subs(so))
        # nontrivial requires: det const != 0 AND W nonconstant (else map is
        # elementary/linear-triangular, hence injective)
        W_nonconst = len(Wv.free_symbols & {x, y}) > 0
        if dv != 0 and W_nonconst:
            interesting += 1
            print(f"   NONTRIVIAL: W={Wv}, lam={so.get(lam,'free')}, det={dv}")
        else:
            print(f"   trivial branch: W={Wv}, det={dv} "
                  f"({'W constant' if not W_nonconst else 'det=0'})")
    if interesting == 0:
        print(f"   ==> VERIFIED: no nontrivial 2D analogue with deg(W) <= {DMAX}")

for d in [2, 3, 4]:
    t0 = time.time()
    probe(d)
    print(f"   ({time.time()-t0:.1f}s)")
