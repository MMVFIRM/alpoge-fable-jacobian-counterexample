# Paper I — The Alpöge–Fable map: an independently checkable counterexample to the Jacobian Conjecture in dimension 3

**Provenance and attribution.** The map was posted publicly by L. Alpöge on
2026-07-19, produced in interaction with an AI system ("Fable"). This package
claims no priority on the map. Its purpose is a *frozen, independently
verifiable certificate*: the central claim reduces to two finite polynomial
computations (Checks 1–2) that any computer algebra system reproduces in
seconds; the remaining checks certify the map's geometry.

## The map

F : C³ → C³, with s = xy, u = 1 + s:

F₁ = u³z + y²u(4+3s)
F₂ = y + 3xu²z + 3xy²(4+3s)
F₃ = 2x − 3x²y − x³z

(coordinate degrees 7, 6, 4).

## The central claim (Checks 1–2 alone carry it)

1. **det J_F = −2**, an exact polynomial identity: F is a Keller map.
   [`checks/check_1_determinant.py`]
2. **F(0, 0, −1/4) = F(1, −3/2, 13/2) = F(−1, 3/2, 13/2) = (−1/4, 0, 0)**,
   with the three points distinct: F is not injective.
   [`checks/check_2_collision.py`]

Together: **the Jacobian Conjecture is false in dimension 3** (and, by adding
dummy variables, in every dimension ≥ 3). Everything below explains the
geometry; nothing below is needed for the central claim.

## The geometry (each item independently certified)

3. **Generic degree 3.** The master identity M(x; F₁,F₂,F₃) ≡ 0 holds in
   C[x,y,z] for M = S̃x³ + (4−3BC)x − 2C, S̃ = 27A²C² − 18ABC + 16A + B³C − B²,
   and M(·;q) is never the zero polynomial — so every fiber has ≤ 3 points
   with x-coordinates among the roots of M. M is irreducible over C(A,B,C);
   an exact Gröbner computation exhibits a rational point with fiber exactly
   3. Field-extension degree = topological degree = 3 (char 0).
   [`checks/check_3_degree.py`]
4. **The exact Jelonek (non-properness) surface** S_F : S̃ = 0 — obtained by
   eliminating the escape direction v from {v² − Bv + 3A, 3Cv² − 4v + B};
   rationally parametrized (uniruled, per Jelonek's general theorem);
   restricting to {A=0} recovers the fiber-drop curves B²(BC−1); the square
   identity 27C²·S̃|_{B=4/(3C)} = (27AC²−4)² locates Γ; the collision point
   lies off S_F. [`checks/check_4_jelonek_surface.py`]
5. **The constructible fiber stratification 3 / 1 / 0** on C³∖S_F, S_F∖Γ,
   Γ = {27AC² = 4, 3BC = 4}: the saturation gate (I_Γ : C^∞) = (1) proves
   from the *original equations* that no point of C³ maps into Γ (so F is
   not surjective — it misses exactly the curve Γ ≅ C*); an explicit
   rational section certifies fiber 1 on S_F∖Γ, with the exact instance
   F⁻¹(1,4,0) = {(0,4,−63)}. [`checks/check_5_stratification.py`]
6. **S₃ structure and transposition monodromy.** disc_x(M) = −4H²S̃ with
   H = 27AC² − 9BC + 8; the squarefree part contains S̃ to the first power,
   so the Galois group of the cubic extension is the full S₃ (the cover is
   non-Galois). Res_A(S̃, H) = 27C²(3BC−4)³ and H|_{C=0} = 8 show H ∩ S_F = Γ,
   so disc vanishes to odd order 1 across generic S_F: the meridian is a
   transposition — an exact parity argument. An exact fiber at an H-point off
   S_F has three distinct preimages with two sharing an x-coordinate: the H²
   factor is a projection artifact, not branching (F is étale everywhere).
   [`checks/check_6_galois.py`]

## Check matrix

| # | Claim | Script | Method | Runtime* |
|---|---|---|---|---|
| 1 | Keller: det J = −2 | check_1 | polynomial expansion | < 10 s |
| 2 | non-injective | check_2 | rational evaluation | < 10 s |
| 3 | degree 3 | check_3 | identity + Gröbner | 1–3 min |
| 4 | Jelonek surface | check_4 | resultants, identities | < 30 s |
| 5 | 3/1/0 strata; misses Γ | check_5 | saturation, section, solve | 1–3 min |
| 6 | S₃, transposition | check_6 | disc parity, exact fibers | ~1 min |

*Python 3.11, SymPy 1.14, single CPU. Every check is a standalone file with
no imports beyond sympy, assert-based, and independent of all others: six
different specialists can verify six different parts. A skeptical referee can
re-implement any check in Magma/Maple/Macaulay2 from the formulas above; no
step depends on floating point (one optional numeric monodromy loop in the
research scripts corroborates item 6 but is not part of the certification —
item 6's parity argument is exact).

## What this paper does NOT claim

All structural consequences (degree minimality, the Jelonek–monodromy–divisor
proof of Campbell's theorem, Orevkov's cubic plane theorem in ledger
language, the constructible defect ledger, the cubic silent-cycle identity,
and the open silent-divisor program) are deliberately excluded and held as
Paper II (`PAPER_II_INDEX.md`), pending outside verification of the present
package. Integrity data for every file is in `MANIFEST.sha256`.
