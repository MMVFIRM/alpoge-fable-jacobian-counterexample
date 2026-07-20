# Proof-grade fiber stratification of the Alpöge–Fable map
(machine-verified 2026-07-20; script `strata.py`. This document SUPERSEDES the
universal fiber claim of `JELONEK_GALOIS.md` §2 and upgrades `LEDGER.md`'s
trichotomy from generic-elimination grade to constructible-proof grade.)

Gate addressed: generic elimination does not automatically survive
specialization to loci where coefficients simultaneously vanish, and an odd
discriminant exponent does not by itself prove branching. Both points are now
resolved from the original equations.

## 0. The master identity (what makes M globally faithful)

With S̃ = 27A²C² − 18ABC + 16A + B³C − B² and
M(x; A,B,C) = S̃x³ + (4−3BC)x − 2C, the polynomial identity

**M(x; F₁(x,y,z), F₂(x,y,z), F₃(x,y,z)) ≡ 0 in C[x,y,z]**

holds (verified by expansion). Moreover M(·;q) is never the zero polynomial in
x: all three coefficients vanishing would force C = 0 and then 4−3BC = 4 ≠ 0.
Consequently, for EVERY target q — with no genericity, no resultant, no
specialization caveat — the x-coordinate of every preimage of q is a root of
M(·; q). (Separately: P1 is monic in U, so the original resultant does
specialize faithfully; but the identity supersedes the point.)

## 1. The saturation gate: Γ-fibers are empty

Γ = {27AC²−4 = 0, 3BC−4 = 0}. With the parametrization A = 4/(27C²),
B = 4/(3C) substituted into the ORIGINAL fiber equations and cleared,
I_Γ = ⟨27C²F₁−4, 3CF₂−4, F₃−C⟩, the saturation (I_Γ : C^∞) computed by
Rabinowitsch (adjoin tC−1) has Gröbner basis **[1]**: the variety is empty.
No point of C³ maps into Γ. This is the exact-ideal confirmation of what the
master identity also gives: M(·;q)|_Γ = −2C ≠ 0 has no roots.

## 2. Existence on S_F ∖ Γ: an explicit section

In the chart ψ(v,a) = (a, (v²+3a)/v, (v²−a)/v³) (which covers S_F minus the
{A=B=0} line, with Γ = {v²=3a}), the unique preimage is given in closed form:

x₀ = 2v(v²−a)/(v²−3a)²,  u₀ = 4av²/(v²−3a)²,
y₀ = B − 3x₀a/u₀,  z₀ = (a/u₀ − y₀²(4+3x₀y₀))/u₀²,

and **F(x₀,y₀,z₀) = ψ(v,a) is verified as an exact identity in (v,a)**. The
combined denominators factor as 16v⁷(v²−3a)²: the section is defined on the
entire chart away from v=0 (the line) and v²=3a (Γ). The remaining strata have
their own exact sections, verified as identities in the stratum parameter:
F(C/2, 0, 0) = (0,0,C) on the line {A=B=0}; F(2/b, −b/2, (10b²−cb³)/8) =
(0,b,c) on {A=0, B≠0} (covering the hyperbola {BC=1}); and {C=0, 16A=B²} is
reached by x=0 points (z+4y², y, 0).

## 3. Uniqueness on S_F ∖ Γ: the shared-x locus is exactly H

Two distinct preimages (u≠0) sharing the same x over the same target require
P1(x,·) | P2(x,·) (P1 monic quadratic). Computing P2 mod P1 = c₁U + c₀ and
eliminating x:

**Res_x(c₁, c₀) = −A²C³·(27AC²−9BC+8) = −A²C³·H.**

So off {A=0}∪{C=0} (strata handled directly above), shared-x forces H = 0.
And H meets S_F only in Γ:

**Res_A(S̃, H) = 27C²(3BC−4)³**, while H|_{C=0} = 8 ≠ 0,

so H ∩ S_F ⊆ {3BC=4} ∩ S_F = Γ (the square identity 27C²·S̃|_{B=4/(3C)} =
(27AC²−4)² from the ledger round). The intersection is a triple contact —
H is tangent to S_F along Γ to third order. Hence on S_F ∖ Γ: M is honestly
linear (slope 4−3BC ≠ 0 there, again by the square identity), all preimages
share its single root x₀, and no two distinct preimages may share x. Fiber
exactly 1.

## 4. What H means off S_F: x-collision, not branching

At q = (−8/27, 0, 1) (on H, off S_F): M(x;q) = −(2/27)(2x+3)(4x−3)², and the
exact fiber is three DISTINCT points:
(−3/2, 4/3, 104/27), (3/4, −2/3+2√3/3, 104/27−8√3/3), (3/4, −2/3−2√3/3, 104/27+8√3/3).
Two sheets share x = 3/4 and differ in (y,z). The factor H² in
disc_x(M) = −4H²S̃ records the failure of x to separate sheets — an artifact
of the projection, not branching. (Multiplicity of the x-root = number of
preimages above it, as the sample shows: 2 over the double root, 1 over the
simple root.)

**Corrected branching argument** (replacing the disc-parity inference): F over
C³∖S_F is a finite étale covering space; the Galois closure of a covering
space is again a covering space of the same base, hence étale over ALL of
C³∖S_F including H∖S_F. It is genuinely branched over S_F because some
meridian must act nontrivially: meridians normally generate π₁ of a
hypersurface complement in C³, so trivial meridian action would force trivial
monodromy and a disconnected degree-3 cover, contradicting connectedness of
C³ minus a surface. The disc factorization remains correct as a *computation*;
the S₃-vs-A₃ conclusion (disc not a square) stands; only the branching claim
needed the covering-space argument.

## 5. The constructible stratification (final)

C³ = U₃ ⊔ U₁ ⊔ U₀:

| stratum | equations | #F⁻¹ | proof |
|---|---|---|---|
| U₃ | S̃ ≠ 0 | 3 | proper étale cover of C³∖S_F; count = degree |
| U₁ | S̃ = 0, (27AC²−4, 3BC−4) ≠ (0,0) | 1 | §2 sections (existence) + §3 (uniqueness) |
| U₀ = Γ | 27AC²−4 = 0, 3BC−4 = 0 | 0 | §0 master identity; §1 saturation gate |

Within U₃, the subvariety {H=0}∖S_F is where two of the three sheets share an
x-coordinate (still 3 distinct preimages). The earlier universal claim
("fiber 1 on all of S_F") is superseded: it holds precisely on S_F∖Γ.

The 3D template is now proof-grade and ready for export to the 2D obstruction
program (degree-2 exclusion draft staged next).
