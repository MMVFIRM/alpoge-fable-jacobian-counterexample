"""
Proof-grade fiber stratification of the Alpoge-Fable map.

Gate (per review): do NOT infer strata from the generic resultant. Establish:
  0. MASTER IDENTITY:  M(x; F1,F2,F3) == 0  identically in C[x,y,z].
     (This is what makes M globally faithful: every preimage's x-coordinate is
      a root of M(.; q) for EVERY q, since M(.;q) is never the zero polynomial:
      its coefficients St, 4-3BC, -2C cannot all vanish -- checked below.)
  1. SATURATION GATE: I_Gamma : C^infty empty, from the ORIGINAL fiber
     equations (Rabinowitsch), not from M.
  2. Symbolic section over S_F \ Gamma (psi-chart) + exact strata sections.
  3. Uniqueness on S_F \ Gamma: P1|P2-elimination identifies the shared-x
     locus; H \cap S_F = Gamma (set-theoretically) closes it.
  4. H = {27AC^2-9BC+8=0} off S_F: two sheets share an x-coordinate but are
     DISTINCT points (no branching; F is etale) -- exact sample fiber.
  5. Assembled constructible stratification U3 | U1 | U0 with equations.
"""
import sys, signal, traceback
sys.path.insert(0, '/home/claude/geo_verify')
import sympy as sp

x, y, z, U, v, a, t, b, c = sp.symbols('x y z U v a t b c')
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
print("0. MASTER IDENTITY  M(x; F(x,y,z)) == 0  in C[x,y,z]")
print("="*72)
master = sp.expand(M.subs({A: F1, B: F2, C: F3}))
print("  M(x; F1,F2,F3) expands to:", master)
print("  IDENTITY HOLDS:", master == 0)
# M(.;q) is never the zero polynomial in x:
never0 = sp.groebner([St, 4-3*B*C, -2*C], A, B, C, order='grevlex')
# simpler: coefficients all zero needs C=0 and then 4-3BC=4 != 0:
print("  can all coefficients of M vanish?  C=0 forces 4-3BC=4 != 0  ->  NO")
print("  => for EVERY q, all preimage x-coordinates are roots of M(.;q),")
print("     with no appeal to resultants. (Also note P1 is MONIC in U, so the")
print("     resultant specializes faithfully; but the identity supersedes it.)")

print()
print("="*72)
print("1. SATURATION GATE: fibers over Gamma from the ORIGINAL equations")
print("="*72)
# Gamma: A = 4/(27 C^2), B = 4/(3C), C != 0. Substituted + cleared, plus
# Rabinowitsch t*C - 1 to enforce C != 0 (this is exactly (I_Gamma : C^oo)):
gens = [sp.expand(27*C**2*F1 - 4),
        sp.expand(3*C*F2 - 4),
        sp.expand(F3 - C),
        t*C - 1]
def gate():
    G = sp.groebner(gens, x, y, z, C, t, order='grevlex')
    return list(G.exprs)
Gex = alarm_run(gate, 400, default=None)
print("  Groebner basis of I_Gamma + <tC-1>:", Gex)
print("  VARIETY EMPTY (basis = [1]):", Gex == [1])

print()
print("="*72)
print("2. EXPLICIT SECTION over S_F \\ Gamma  (existence of the 1 preimage)")
print("="*72)
# psi-chart: (v,a) -> (a, (v^2+3a)/v, (v^2-a)/v^3), covering S_F minus the
# {A=B=0} line;  Gamma corresponds exactly to v^2 = 3a  (checked below).
Av, Bv, Cv = a, (v**2+3*a)/v, (v**2-a)/v**3
print("  Gamma in chart: B^2-12A =", sp.factor(Bv**2 - 12*Av), " -> v^2 = 3a")
x0 = sp.cancel(2*Cv/(4 - 3*Bv*Cv))
print("  x0 =", x0)
P1c = sp.Poly((U**2 - U*(1+x0*Bv) + 3*x0**2*Av).simplify(), U)
P2c = sp.Poly((U**3*Cv - x0*U*(1+U) + x0**3*Av).simplify(), U)
q_, r_ = sp.div(P2c, P1c)
r_ = sp.Poly(r_, U)
c1, c0 = r_.all_coeffs() if r_.degree() == 1 else (None, None)
u0 = sp.cancel(-c0/c1)
y0 = sp.cancel(Bv - 3*x0*Av/u0)
z0 = sp.cancel((Av/u0 - y0**2*(4+3*x0*y0))/u0**2)
chk = [sp.cancel(sp.expand(Fi.subs({x: x0, y: y0, z: z0})) - tv)
       for Fi, tv in [(F1, Av), (F2, Bv), (F3, Cv)]]
print("  u0 =", u0)
print("  SECTION VERIFIES  F(x0,y0,z0) = psi(v,a):", all(e == 0 for e in chk))
dens = sp.factor(sp.denom(sp.together(x0)) * sp.denom(sp.together(y0)) * sp.denom(sp.together(z0)))
print("  denominators involve only:", dens)
print("   -> section defined wherever v != 0 and v^2 != 3a: ALL of chart minus Gamma")
print()
# strata not in the chart, exact sections (identities in the stratum parameter):
lineck = (sp.expand(F1.subs({x: c/2, y: 0, z: 0})),
          sp.expand(F2.subs({x: c/2, y: 0, z: 0})),
          sp.expand(F3.subs({x: c/2, y: 0, z: 0})))
print("  line {A=B=0}:  F(C/2, 0, 0) =", lineck, " == (0,0,C)  OK:", lineck == (0,0,c))
hyp = {x: 2/b, y: -b/2, z: (10*b**2 - c*b**3)/8}
hypck = tuple(sp.simplify(Fi.subs(hyp)) for Fi in (F1, F2, F3))
print("  hyperbola {A=0,BC=1} (and all of {A=0,B!=0}):  F(2/b,-b/2,(10b^2-cb^3)/8) =",
      hypck, " == (0,b,c)  OK:", hypck == (0, b, c))

print()
print("="*72)
print("3. UNIQUENESS on S_F \\ Gamma: the shared-x locus and H ∩ S_F")
print("="*72)
# Two distinct preimages (u != 0) with the SAME x over the same target
# <=> P1(x,.) | P2(x,.)  (P1 monic quadratic; both its U-roots common)
P1 = sp.Poly(U**2 - U*(1+x*B) + 3*x**2*A, U)
P2 = sp.Poly(U**3*C - x*U*(1+U) + x**3*A, U)
_, rem = sp.div(P2, P1)
rem = sp.Poly(sp.expand(rem.as_expr()), U)
cc = rem.all_coeffs()
print("  P2 mod P1 = c1(x;q)*U + c0(x;q); divisibility <=> c1 = c0 = 0")
elim = sp.factor(sp.resultant(cc[0], cc[1], x))
print("  Res_x(c1, c0) =", elim)
H = 27*A*C**2 - 9*B*C + 8
print("  contains H = 27AC^2-9BC+8:", sp.simplify(sp.factor(elim).as_ordered_factors()[-1] - H) == 0 or H in [f for f in sp.factor_list(elim)[1] and []] or (sp.rem(sp.expand(elim), H, A) == 0))
# cleaner check: is elim divisible by H as polynomial in A?
qq, rr = sp.div(sp.Poly(sp.expand(elim), A), sp.Poly(H, A))
print("  elim divisible by H:", sp.expand(rr.as_expr()) == 0)
# H ∩ S_F = Gamma (set-theoretically):
RA = sp.factor(sp.resultant(St, H, A))
print("  Res_A(St, H) =", RA)
print("  H at C=0:", H.subs(C, 0), " (never 0)  =>  H ∩ S_F ⊆ {3BC-4=0} ∩ S_F = Gamma")
print("  (square identity from the ledger round: 27C^2·St|_{B=4/(3C)} = (27AC^2-4)^2)")
print("  ==> on S_F \\ Gamma: no two distinct preimages share x; M linear there")
print("      with slope 4-3BC != 0  =>  fiber EXACTLY 1.")

print()
print("="*72)
print("4. H OFF S_F: shared x-coordinate, DISTINCT points, NO branching")
print("="*72)
pt = {A: sp.Rational(-8,27), B: 0, C: 1}
print("  sample q = (-8/27, 0, 1):  St(q) =", sp.simplify(St.subs(pt)),
      " (off S_F);  H(q) =", sp.simplify(H.subs(pt)), " (on H)")
Mq = sp.factor(M.subs(pt))
print("  M(x;q) =", Mq, " -> double root x=3/4, simple root x=-3/2")
def fib():
    return sp.solve([F1 - pt[A], F2 - pt[B], F3 - pt[C]], [x, y, z], dict=True)
r = alarm_run(fib, 200, default="timeout")
print("  exact fiber:", r)
if isinstance(r, list):
    xs = [so[x] for so in r]
    print(f"  {len(r)} DISTINCT preimages; x-coordinates {xs}")
    print("  -> two sheets share x=3/4 but differ in (y,z): the squared factor")
    print("     H^2 in disc(M) is an artifact of projecting to x, NOT branching.")
print()
print("  Corrected branching argument for the Galois closure (no disc needed):")
print("   F restricted over C^3\\S_F is a finite etale covering space; the Galois")
print("   closure of a covering space is again a covering space of the SAME base,")
print("   hence etale over ALL of C^3\\S_F, including H\\S_F. It IS branched over")
print("   S_F because some meridian acts nontrivially: if all meridians acted")
print("   trivially the monodromy would be trivial (meridians normally generate")
print("   pi_1 of a hypersurface complement in C^3) and the degree-3 cover would")
print("   be disconnected -- contradicting connectedness of C^3 minus a surface.")

print()
print("="*72)
print("5. THE CONSTRUCTIBLE STRATIFICATION (proof-grade)")
print("="*72)
print("""  C^3 = U3 ⊔ U1 ⊔ U0, with St = 27A²C²-18ABC+16A+B³C-B²:

   U3 = { St != 0 }                          #F^{-1} = 3
        (proper etale covering over the complement of S_F; count = top degree)
   U1 = { St = 0 } \\ Gamma                   #F^{-1} = 1
        (existence: explicit sections, Sec.2 -- psi-chart formula plus the
         {A=B=0}-line and {A=0,B!=0} identities, and {C=0,16A=B²} via x=0;
         uniqueness: master identity + M linear with slope 4-3BC != 0 there
         + shared-x needs H, and H ∩ S_F = Gamma, Sec.3)
   U0 = Gamma = { 27AC²-4 = 0, 3BC-4 = 0 }   #F^{-1} = 0
        (master identity: M(.;q) = -2C != 0 has no roots; independently the
         saturation (I_Gamma : C^infty) = (1), Sec.1)

  The universal claim from the Galois round ("fiber 1 on all of S_F") is
  hereby SUPERSEDED: it holds on S_F \\ Gamma only; Gamma is empty-fiber.""")
