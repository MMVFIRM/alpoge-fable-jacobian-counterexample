# The exact image, the Euler ledger, and the 2D obstruction demo
(computed & machine-verified 2026-07-20; script: `ledger.py`; continues
`JACOBIAN_STRUCTURE.md` and `JELONEK_GALOIS.md`)

## 0. A correction, first

In the structure round I reported the Alpöge–Fable map "appears surjective — no
missed values found." That was wrong, and this round's machinery found the miss
exactly. The numeric probes never landed on a measure-zero curve; the fiber
cubic finds it symbolically.

## 1. The exact image: F misses precisely the cusp curve of its Jelonek set

On {4−3BC=0}, the identity 27C²·S̃|_{B=4/(3C)} = (27AC²−4)² shows
S_F ∩ {4−3BC=0} = D := {A = 4/(27C²), B = 4/(3C)} — which is exactly
Sing(S_F), the cuspidal edge. On D the fiber cubic collapses to the nonzero
constant M|_D = −2C: **no preimages**. Edge cases closed exactly (x=0 reaches
only {C=0}, disjoint from D; u=0 preimages need A=0, impossible on D), and two
Gröbner solves confirm empty fibers at rational points of D.

**Image(F) = C³ ∖ D.** The counterexample is not surjective: it misses exactly
one closed rational curve D ≅ C* — the singular locus of its own non-properness
set. It is the polynomial sibling of exp: C → C∖{0}, one dimension up.

Fiber trichotomy, now exact by root-counting of M = S̃x³ + (4−3BC)x − 2C:
**3** preimages on C³∖S_F, **1** on S_F∖D (M becomes honest linear), **0** on D.

## 2. The Euler-characteristic ledger balances to the penny

χ(S_F) = 1: S_F decomposes as ψ(C*×C) ⊔ {A=B=0 line}, where
ψ(v,A) = (A, (v²+3A)/v, (v²−A)/v³) is bijective onto its image (gcd checks:
unique escape direction v at generic points, double root exactly on the
cuspidal edge D; the line is disjoint from im ψ since B=0 forces A=−v²/3≠0).
So χ(S_F) = χ(C*×C) + χ(line) = 0 + 1 = 1, and χ(D) = χ(C*) = 0.

**Ledger:** χ(C³) = 3·χ(C³∖S_F) + 1·χ(S_F∖D) + 0·χ(D):
1 = 3(1−1) + (1−0) + 0 = 1. **Balanced.**

## 3. The 2D obstruction demo: a would-be counterexample, detected

Slice by the generic plane H: A = 1 + B/2 − C/3. Then X := F⁻¹(H) is a smooth
connected rational affine surface with an étale degree-3 map X → H ≅ C² — this
is *exactly what a 2D counterexample would be if X were C²*. Computed:

- S_H = S_F ∩ H is an **irreducible quartic with exactly 3 cusps** (the three
  points of H ∩ D; Hessian degenerate at each; no other singular points by
  resultant sweep), smooth at infinity with 4 distinct points there.
- Genus g = 3 − 3 = 0 (rational), χ(S_H^proj) = 2, **χ(S_H) = 2 − 4 = −2**.
- Ledger for X: χ(X) = 3(1−(−2)) + (−2−3) + 0 = **4 ≠ 1 = χ(C²)**.

The Euler obstruction is what "sees" that X is not C². A genuine 2D
counterexample would need its own ledger to balance with χ(X) = 1.

## 4. The 2D program, stated

A hypothetical étale degree-d counterexample F: C²→C² must satisfy:
(i) 1 = d(1 − χ(S)) + Σₖ k·χ(Sₖ) over the preimage-count strata;
(ii) every component of S is a polynomially parametrized rational curve
(Jelonek), so χ(component) ≤ 1; (iii) π₁(C²∖S) → S_d transitive, meridians
moving exactly the escaping sheets, discriminant parity constraining the image;
(iv) the fiber polynomial's leading coefficient cuts out S. The 3D
counterexample satisfies all four with (χ_S, χ_D, d) = (1, 0, 3). In 2D these
soft constraints do not yet close to a contradiction (χ of curves can be
negative) — that residue is where the open problem lives. The low-sheeted 2D
cases connect to the exotic-covering literature (Orevkov and collaborators
studied low-degree "exotic coverings" over C²; Newton–Puiseux chart methods
apply to the Jacobian problem).

## 5. Honest scope

Exact: the square identity, M's degeneration on each stratum, both empty-fiber
Gröbner checks, the fiber trichotomy, χ(S_F)=1 and χ(D)=0 (given the ψ
stratification, whose injectivity/disjointness steps are symbolically checked),
the balanced ledgers, S_H's cusp count/smoothness-at-infinity (numeric roots
with exact spot-checks), irreducibility of S_H. Assumed-classical: δ=1 for A₂
cusps in the genus count. Not claimed: any progress on 2D JC itself; priority
on any of this (the community is certainly computing in parallel).
