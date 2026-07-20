# The constructible defect ledger
(per reviewer specification; machine verifications in `defect_ledger.py`;
continues STRATA.md / DEGREE3_PLANE.md)

## Headline theorem (Gate 1): Constructible Defect Ledger

For every quasi-finite polynomial map F: Cⁿ → Cⁿ of generic degree d, define
the **defect function** δ_F(q) = d − #F⁻¹(q). As constructible functions,

**δ_F = d·1_{Cⁿ} − F_! 1_{Cⁿ}**,

and Euler integration gives the exact all-dimensional identity

**∫_{Cⁿ} δ_F dχ_c = d − 1.**

*Proof.* Quasi-finiteness makes (F_!1)(q) = χ_c(F⁻¹(q)) = #F⁻¹(q), a
constructible function. Functoriality of Euler integration
(∫ F_!φ dχ_c = ∫ φ dχ_c) gives ∫ F_!1 = χ_c(Cⁿ_source) = 1, so
∫δ_F = d·χ_c(Cⁿ) − 1 = d − 1. Equivalently: χ_c(source) = Σ k·χ_c(Y_k) and
χ_c(target) = Σ χ_c(Y_k) over the fiber-count strata Y_k = {q : #F⁻¹(q) = k};
subtract. ∎ (Standard Euler-calculus machinery; the étale hypothesis is NOT
needed for the scalar identity — only for the dictionary below.)

For an étale map, the generic defect on each divisorial stratum equals the
total size of the escaping meridian orbits, including silent length-one
orbits (Gate 2).

**Fable instantiation:** Y₃ = C³∖S_F, Y₁ = S_F∖Γ, Y₀ = Γ:
2 = 2χ_c(S_F∖Γ) + 3χ_c(Γ) = 2χ_c(S_F) + χ_c(Γ) = 2·1 + 0. The affine shadow
of the ledger rounds is now a theorem, not an observation. And the scalar
identity's coarseness is exhibited immediately: **3χ_c(Γ) = 0 — the missed
curve is invisible to the scalar ledger** despite being structurally
essential. Hence Gates 2–4.

## Gate 2: Divisorial dictionary

Let X = Norm(cl Γ_F) ⊂ Pⁿ × Cⁿ with proper projection F̄ and boundary
B = X ∖ Cⁿ. **Claim:** each boundary divisor E ⊆ B dominating a component
D ⊆ S_F carries generic relative multiplicity μ_E equal to the meridian-orbit
length of the corresponding escape branch, and at a generic point of D,
δ_D = Σ_{E↦D} μ_E. *(Rigor label: dictionary-grade — the orbit/μ
correspondence is proved at the level of Puiseux branches over transverse
lines; the full normalization of the graph closure has not been computed for
the Fable map. The general proof route: an escape orbit of length k is one
analytic branch of F̄⁻¹(transverse line) through the boundary, meeting E with
local intersection multiplicity k.)*

**Fable instantiation (verified):** escaping sheets go to infinity with
u ~ v·x and **y → v, where v² − Bv + 3A = 0 — the escape direction IS the
Jelonek chart parameter.** Numerically at (1.01, 4, 0): the two escaping
sheets have y = 1 ± 0.3i → v = 1 while the surviving sheet is at x ≈ 0. The
swap monodromy makes the two escape branches one Puiseux orbit: **one
boundary divisor E over S_F, μ_E = 2 = δ generic.** Dictionary holds.

## Gate 3: Jump strata

Bad-divisor stratification by: additional branches escaping; surviving
branches disappearing; boundary components meeting; image singularities;
multiplicity jumps. Target form: d − 1 = Σ_α δ_α χ_c(S_α).

**Fable jump table (verified):**

| stratum | δ | mechanism |
|---|---|---|
| S_F ∖ Γ | 2 | one length-2 escape orbit |
| Γ | 3 | (i) the two escape directions **collide** (B²−12A ≡ 0 on Γ: v-double root); (ii) the surviving section escapes (its denominator (v²−3a)² vanishes exactly on Γ) |

Both mechanisms from the reviewer's taxonomy occur at Γ simultaneously —
Γ is where the boundary divisor E is pinched AND where a surviving branch
disappears.

## Gate 4: Sliced ledger — the defect class

For generic affine L of dimension m, record ∫_L δ_F dχ_c. This general-
linear-section Euler data is equivalent to CSM/polynomial-Chern-class-level
information (Aluffi), upgrading the scalar to a class-valued invariant.

**Defect class of the Fable map (verified, with independent cross-checks):**

| m | ∫_L δ dχ_c | cross-check |
|---|---|---|
| 0 | 0 | generic point off S_F |
| 1 | **8** | = 2·deg S_F; and 3 − χ(F⁻¹(L)) with χ = 3(1−4)+4 = −5 ✓ |
| 2 | **−1** | = 2(χ(S_H)−3) + 9; and 3 − χ(X_H) = 3 − 4 ✓ |
| 3 | **2** | = d − 1 (Gate 1) |

**δ̂(Fable) = (0, 8, −1, 2).** The m=2 entry sees Γ (contribution +9 from the
three points H∩Γ) — the missed curve, invisible at m=3, is visible in every
generic plane slice. The m=1 entry is the **defect-degree**
Σ_{divisorial α} δ_α·deg S_α = 2·4 = 8, a Bézout-type quantity bounded by the
coordinate degrees through χ(F⁻¹(L)) — a quantitative handle for future use.

## Complete instantiations (all four objects, all balanced)

| object | type | strata (δ ≠ 0) | stratified sum |
|---|---|---|---|
| Fable map | étale, d=3 | S_F∖Γ: 2; Γ: 3 | 2·1 + 3·0 = **2** ✓ |
| silent model εx³+x²+x+c | branched cover, d=3 | Δ∖(2 pts): 1 (merge); {ε=0}∖pt: 1 (silent escape); (0,¼): 2; (⅓,⅓): 2 | (0−2) + 0 + 2 + 2 = **2** ✓ |
| transposition model εx³+4x−2c | branched cover, d=3 | Δ ≅ C*: 1 (merge); {ε=0}: 2 (escape orbit) | 0 + 2 = **2** ✓ |
| resolvent G=(p,−t³−tp) | proper, non-Keller | K∖0: 1; cusp: 2 (all merge) | 0 + 2 = **2** ✓ |

Supporting exact facts verified: the silent model's discriminant curve is
rationally parametrized by the double root (disc∘param ≡ 0), has
χ_c(Δ) = −1 + 1 = 0 (parameter domain C∖{0,−½} plus the limit point
(ε,c) → (0,¼) as r → −½, computed exactly), and its triple-root point is
exactly (⅓,⅓) (M = (x+1)³/3). The transposition model's Δ ≅ C* is disjoint
from the divisor and admits no triple roots.

**The lesson of the table:** the defect function cannot distinguish merge
from escape — the silent model and the resolvent spend the same budget by
merging that a Keller map must spend by escaping. Étaleness closes the merge
channel; that is precisely why the dictionary (Gate 2) and not the scalar
(Gate 1) carries the Keller-specific content.

## The upgrade, and the reframed silent-divisor question

**Orevkov's numerical budget ⟶ an all-dimensional constructible defect
object.** The scalar identity generalizes his N−1 accounting to every
dimension; the dictionary identifies μ with orbit lengths; the jump strata
carry the exceptional terms; the sliced class recovers what χ_c-blindness
loses (Γ!).

The universal silent-divisor question is now better posed: not "do silent
divisors exist?" but **"which defect classes δ̂ can contain a silent
divisorial stratum (δ = 1 contribution at m = 1 per unit degree) while
satisfying the global graph-at-infinity ledger?"** The micro-model shows
silent escape is locally coherent; any exclusion must be global, and the
defect class is the natural global invariant to constrain it. Concrete first
question: for étale d = 3 in C³, is there a consistent δ̂ with a silent
stratum, or does the S₃/parity structure (disc-invisibility of silent
branches, Gate-2 dictionary) force the Fable pattern δ̂ = (0, 2·deg S, ·, 2)?

## Status

Theorem-grade: Gate 1 and all four instantiations; the Fable jump table; the
defect class computation with cross-checks. Dictionary-grade: Gate 2's
general claim (proved on transverse-line branches; graph-closure
normalization not computed). Classical inputs: Euler calculus / constructible
functions (MacPherson; Curry–Ghrist–Robinson), CSM/linear-section
correspondence (Aluffi). Plane-status corrections adopted from review:
Domrina (2000) for four sheets; Żołądek for topological degree ≤ 5; the
five-sheeted exotic covering marks the limit of bare covering topology. No
priority claims; the community is verifying the underlying map in parallel.
