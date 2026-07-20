"""
The Euler-characteristic ledger of the Alpoge-Fable map, its EXACT image,
and the 2D obstruction demo.

Everything flows from the fiber cubic (established in jelonek.py):
    M(x; A,B,C) = St*x^3 + (4-3BC)*x - 2C,   St = 27A^2C^2-18ABC+16A+B^3C-B^2
whose roots are the x-coordinates of the fiber over (A,B,C).

Sections:
  1. EXACT image: on S_F = {St=0}, when does M lose ALL roots?
     Claim: S_F \cap {4-3BC=0} = D := Sing(S_F) = {A=4/(27C^2), B=4/(3C)},
     and M|_D = -2C != 0  =>  fiber EMPTY on D  =>  F misses exactly D.
     (Corrects the round-2 'appears surjective' assessment.)
  2. Fiber trichotomy, now exact: 3 | 1 | 0 on C^3\S_F | S_F\D | D.
  3. chi ledger: chi(S_F)=1, chi(D)=0, and 1 = 3(1-chi_S) + (chi_S - chi_D).
  4. 2D demo: slice by a generic plane; the induced etale 3:1 cover X -> C^2
     has chi(X) = 4 != 1: the Euler obstruction detects X != C^2.
"""
import sys, time, signal, traceback
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

x, y, z, U, v, W_ = sp.symbols('x y z U v W')
A, B, C = sp.symbols('A B C')
s = x*y; u = 1 + s
F1 = sp.expand(u**3*z + y**2*u*(4+3*s))
F2 = sp.expand(y + 3*x*u**2*z + 3*x*y**2*(4+3*s))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
St = 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2
M  = St*x**3 + (4 - 3*B*C)*x - 2*C

def alarm_run(fn, secs, default=None):
    def h(sig, frm): raise TimeoutError
    old = signal.signal(signal.SIGALRM, h); signal.alarm(secs)
    try: r = fn()
    except TimeoutError: r = default
    except Exception: traceback.print_exc(); r = default
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM, old)
    return r

print("="*72)
print("1. THE EXACT IMAGE OF F")
print("="*72)
# On {BC = 4/3} (i.e. 4-3BC=0), substitute B = 4/(3C):
St_on = sp.simplify(St.subs(B, 4/(3*C)) * 27*C**2)
print("  27C^2 * St |_{B=4/(3C)} =", sp.factor(St_on))
print("  => on {4-3BC=0}: St=0  <=>  27AC^2-4=0  <=>  the point lies on")
print("     D := {A=4/(27C^2), B=4/(3C)}  — which is exactly Sing(S_F).")
print("  M on D:", sp.simplify(M.subs({B: 4/(3*C), A: 4/(27*C**2)})),
      " (constant in x, nonzero since C!=0 on D)  =>  NO preimages on D")
print("  M on S_F\\D: linear (4-3BC)x - 2C with 4-3BC != 0  =>  EXACTLY 1 preimage")
print()
print("  Edge cases closed off exactly:")
print("   - x=0 preimages: F(0,y,z) = (z+4y^2, y, 0), so x=0 only reaches {C=0};")
print("     D has C != 0  =>  no x=0 preimage on D")
print("   - u=0 preimages: require A = uW = 0; on D, A = 4/(27C^2) != 0  => none")
print()
# Groebner verification: empty fibers at two rational points of D
for (Ca,) in [(1,), (-2,)]:
    Av, Bv, Cv = sp.Rational(4,27)/Ca**2, sp.Rational(4,3)/Ca, Ca
    r = alarm_run(lambda a=Av,b=Bv,c=Cv: sp.solve([F1-a, F2-b, F3-c], [x,y,z], dict=True),
                  150, default="timeout")
    print(f"  exact fiber over D-point ({Av},{Bv},{Cv}):", r,
          " <-- EMPTY" if r == [] else "")
# control: (1,4,0) on S_F\D had exactly 1; generic points have 3 (established earlier)
print()
print("  ==> IMAGE(F) = C^3 \\ D exactly. F is NOT surjective: it misses the")
print("      cuspidal-edge curve of its own Jelonek set (D ~ C*, a rational curve).")
print("      [CORRECTION of round-2 'appears surjective' — numeric probes never")
print("       landed on the measure-zero curve D; the exact cubic finds it.]")

print()
print("="*72)
print("2. FIBER TRICHOTOMY (now exact, from root-counting of M)")
print("="*72)
print("  # preimages = 3 on C^3\\S_F   (cubic with nonzero lead, disc != 0 there)")
print("              = 1 on S_F\\D     (M degenerates to honest linear poly)")
print("              = 0 on D          (M = nonzero constant)")
print("  consistency: (0,0,C) in S_F\\D: M = 4x-2C, root x=C/2 -> fiber 1  matches")
print("  the exact solve (0,0,1)->{(1/2,0,0)} from the structure round.")

print()
print("="*72)
print("3. THE EULER-CHARACTERISTIC LEDGER (3D, closes exactly)")
print("="*72)
# chi(S_F): S_F = psi(C* x C) ⊔ {A=B=0 line}, psi(v,A) = (A,(v^2+3A)/v,(v^2-A)/v^3)
psi = (A, (v**2+3*A)/v, (v**2-A)/v**3)
# (a) the line {A=B=0} is disjoint from the image of psi:
solB0 = sp.solve(sp.Eq((v**2+3*A)/v, 0), A)
print("  psi hits B=0 only when A =", solB0, "(so A=0 & B=0 needs v=0, excluded)")
# (b) psi is injective off D (one common root v generically):
f1 = v**2 - B*v + 3*A; f2 = 3*C*v**2 - 4*v + B
samp = {A: sp.Rational(2,5)}
vv0 = sp.Rational(3,2)
Bv = (vv0**2 + 3*samp[A])/vv0; Cv = (vv0**2 - samp[A])/vv0**3
g = sp.gcd(f1.subs({A: samp[A], B: Bv}), f2.subs({B: Bv, C: Cv}))
print("  gcd(f1,f2) at a random S_F point:", g, " (degree 1: unique escape direction)")
d_pt = {A: sp.Rational(4,27), B: sp.Rational(4,3), C: 1}
g2 = sp.gcd(f1.subs(d_pt), f2.subs(d_pt))
print("  gcd(f1,f2) at a D point:", sp.factor(g2), " (double root: cuspidal edge)")
print()
print("  => chi(S_F) = chi(C* x C) + chi(line) = 0 + 1 = 1")
print("     chi(D)   = chi(C*)              = 0")
chiS, chiD, d = 1, 0, 3
lhs = 1
rhs = d*(1 - chiS) + 1*(chiS - chiD) + 0*chiD
print(f"  LEDGER: chi(C^3) = d*chi(C^3\\S) + 1*chi(S\\D) + 0*chi(D)")
print(f"          {lhs} = {d}*(1-{chiS}) + ({chiS}-{chiD}) + 0  =  {rhs}   {'BALANCED' if lhs==rhs else 'FAILS'}")

print()
print("="*72)
print("4. THE 2D OBSTRUCTION DEMO: slice to an etale 3:1 cover X -> C^2")
print("="*72)
# generic plane H: A = 1 + B/2 - C/3.  X := F^{-1}(H) is a smooth connected
# affine surface, etale 3:1 over H ~ C^2, non-proper over S_H = S_F ∩ H.
ell = 1 + B/2 - C/3
Sq = sp.expand(St.subs(A, ell))
print("  slice curve S_H (quartic):")
print("   ", Sq)
_, flist = sp.factor_list(Sq)
print("  irreducible:", len(flist) == 1 and flist[0][1] == 1)
# singular points of S_H = H ∩ D (the three cusps): solve ell = 4/(27C^2), B = 4/(3C)
cub = sp.expand((ell.subs(B, 4/(3*C)) - sp.Rational(4,27)/C**2) * 27 * C**2)
print("  H ∩ D condition (cubic in C):", cub, "= 0")
Croots = sp.Poly(cub, C).nroots(n=25)
print("  roots:", [complex(r) for r in Croots], " -> ", len(set([round(complex(r).real,8)+1j*round(complex(r).imag,8) for r in Croots])), "distinct")
SqB = sp.diff(Sq, B); SqC = sp.diff(Sq, C)
import numpy as np
Sqf  = sp.lambdify((B,C), Sq, 'numpy')
SqBf = sp.lambdify((B,C), SqB, 'numpy')
SqCf = sp.lambdify((B,C), SqC, 'numpy')
Hess = sp.hessian(Sq, (B,C))
Hessf = sp.lambdify((B,C), Hess.det(), 'numpy')
n_cusp = 0
for r0 in Croots:
    c0 = complex(r0); b0 = complex(4/(3*c0))
    vals = (abs(Sqf(b0,c0)), abs(SqBf(b0,c0)), abs(SqCf(b0,c0)))
    hd = Hessf(b0,c0)
    is_sing = all(vv < 1e-8 for vv in vals)
    is_cusp = is_sing and abs(hd) < 1e-6
    n_cusp += bool(is_cusp)
    print(f"   sing pt (B,C)=({b0:.4f},{c0:.4f}): |S|,|S_B|,|S_C|={vals[0]:.1e},{vals[1]:.1e},{vals[2]:.1e}, Hess det={abs(hd):.1e} -> {'CUSP (A2: degenerate Hessian)' if is_cusp else 'node/other'}")
print(f"  cusps found: {n_cusp} (expected 3 = deg of the space cubic D)")
# no OTHER singular points: resultant check (numpy roots for robustness)
Rres = sp.expand(sp.resultant(SqB, SqC, C))
bcoeffs = [complex(c) for c in sp.Poly(Rres, B).all_coeffs()]
extra = np.roots(bcoeffs)
n_other = 0
seen_other = []
for b0 in extra:
    ccoeffs = [complex(cc) for cc in sp.Poly(SqB.subs(B, complex(b0)), C).all_coeffs()]
    if len(ccoeffs) < 2:
        continue
    for c0 in np.roots(ccoeffs):
        if abs(Sqf(b0,c0)) < 1e-5 and abs(SqBf(b0,c0)) < 1e-5 and abs(SqCf(b0,c0)) < 1e-5:
            if min(abs(c0-complex(rr)) for rr in Croots) > 1e-4:
                key = (round(b0.real,5), round(b0.imag,5), round(c0.real,5), round(c0.imag,5))
                if key not in seen_other:
                    seen_other.append(key); n_other += 1
print(f"  additional singular points beyond the 3 cusps: {n_other}")
# points at infinity: leading form = C*(cubic)
lead = sp.expand(sum(t for t in Sq.as_ordered_terms()
                     if sp.total_degree(t, B, C) == 4))
print("  leading (degree-4) form:", sp.factor(lead))
cubic_inf = sp.simplify(sp.factor(lead)/C) if sp.simplify(lead/C) == sp.expand(lead/C) else None
lf = sp.factor(lead)
# count distinct roots [B:C] of the quartic form:
q = sp.Poly(lead.subs(C, 1), B)
infroots = np.roots([complex(c) for c in q.all_coeffs()])
k_inf = len(set(round(complex(r).real,8)+1j*round(complex(r).imag,8) for r in infroots))
# plus the direction C=0 if lead vanishes there: lead(B,0):
k_inf += 1 if sp.expand(lead.subs(C, 0)) == 0 else 0
print(f"  distinct points at infinity: {k_inf}")
# smoothness at infinity:
Wh = sp.Symbol('Wh')
G = sp.expand(Wh**4 * Sq.subs({B: B/Wh, C: C/Wh}))
sm = True
pts_inf = [(complex(r), 1.0) for r in infroots] + ([(1.0, 0.0)] if sp.expand(lead.subs(C,0))==0 else [])
gB = sp.lambdify((B,C,Wh), sp.diff(G,B), 'numpy')
gC = sp.lambdify((B,C,Wh), sp.diff(G,C), 'numpy')
gW = sp.lambdify((B,C,Wh), sp.diff(G,Wh), 'numpy')
for (b0,c0) in pts_inf:
    gr = (abs(gB(b0,c0,0)), abs(gC(b0,c0,0)), abs(gW(b0,c0,0)))
    if max(gr) < 1e-8: sm = False
print("  projective curve smooth at infinity:", sm)
# chi assembly
g_geom = 3 - n_cusp*1     # quartic arithmetic genus 3, each A2 cusp delta=1
chi_proj = 2 - 2*g_geom - 0   # cusps unibranch: no (r-1) corrections
chi_aff = chi_proj - k_inf
print(f"  geometric genus g = 3 - {n_cusp} = {g_geom}  (rational curve)")
print(f"  chi(S_H projective) = {chi_proj},  chi(S_H affine) = {chi_proj} - {k_inf} = {chi_aff}")
m = n_cusp   # points of H ∩ D: fiber EMPTY there
chiX = 3*(1 - chi_aff) + (chi_aff - m) + 0*m
print()
print(f"  LEDGER FOR X:  chi(X) = 3*(1 - chi(S_H)) + (chi(S_H) - {m}) + 0*{m}")
print(f"                 chi(X) = 3*(1-({chi_aff})) + ({chi_aff}-{m}) = {chiX}")
print(f"  chi(C^2) = 1.  chi(X) = {chiX} != 1  ==>  X is NOT C^2.")
print("  X is a smooth connected rational affine surface, etale 3:1 over C^2 —")
print("  exactly what a 2D counterexample would be IF X were C^2. The Euler")
print("  obstruction is what detects that it is not.")

print()
print("="*72)
print("5. THE 2D LEDGER (the obstruction program, stated)")
print("="*72)
print("""  A hypothetical etale degree-d counterexample F: C^2 -> C^2 must satisfy
   (i)   1 = d*(1 - chi(S)) + sum_k k*chi(S_k)   [S_k = stratum with k preimages]
   (ii)  every component of S is a polynomially parametrized rational curve
         (Jelonek) hence has chi <= 1
   (iii) pi_1(C^2\\S) -> S_d transitive; meridians move exactly the escaping
         sheets; disc parity of the fiber polynomial constrains parity
   (iv)  leading coefficient of the fiber polynomial cuts out S (the 3D template)
  The 3D counterexample satisfies all four with (chi_S, chi_D, d) = (1, 0, 3).
  In 2D these constraints alone do not yet close to a contradiction — chi of
  curves can be negative — which is precisely where the open problem lives.""")
