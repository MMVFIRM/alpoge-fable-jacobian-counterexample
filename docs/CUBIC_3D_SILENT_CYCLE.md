# The cubic divisorial trichotomy and the silent-cycle identity
(per reviewer specification; machine verifications in `cubic_silent.py`;
continues DEFECT_LEDGER_3D.md)

Throughout: F: C³ → C³ étale (Keller) of generic degree 3, S_F its Jelonek
hypersurface (Jelonek: nonempty, uniruled), D an irreducible component.

## Gate 1: Cubic divisorial trichotomy (theorem-grade)

At a generic point of D, the meridian acts on the three sheets. Fixed-point-
free meridians (3-cycles) are banned by the fixed-sheet corollary; orbits of
converging sheets are banned by L2-uniformity; L3 bans generic fiber 0. The
complete case list at generic points of D:

| Type | Meridian | Escaping sheets | Generic fiber | Defect δ |
|---|---|---|---|---|
| T | transposition | one orbit of length 2 | 1 | 2 |
| S₁ | identity | one silent singleton | 2 | 1 |
| S₂ | identity | two silent singletons | 1 | 2 |

Exclusivity: a T-meridian's fixed sheet must converge (else fiber 0, banned),
so there is no T/silent hybrid; generic defect 3 is forbidden. Global S₃
monodromy forces at least one T-component. Nothing in transitivity forbids
S₁ or S₂ components — and the parity table shows why discriminant data alone
cannot: **T is disc-visible (odd order); S₁ and S₂ are disc-invisible (orders
0 and 2 in the verified micro-models — the S₂ model (εx−1)(εx−2)(x−c) has
disc = ε²(cε−2)²(cε−1)², a perfect square); T and S₂ carry the same defect.**

## Gate 2: The intrinsic branch divisor (upgraded to theorem-grade)

By Zariski's Main Theorem, the quasi-finite F factors as an open immersion
into a finite map: C³_source ↪ Y →^ν C³_target, where Y = the normalization
of the target in C(x,y,z), boundary B = Y ∖ C³_source. F étale ⇒ ν is
unramified on the source part, so the ramification divisor R_ν lies in B.

**Puiseux–ramification bridge (the upgrade).** At a generic point of D take a
transverse algebraic line with local parameter ε. The fiber algebra of ν over
C((ε)) factors into finite field extensions of C((ε)); by Newton–Puiseux,
irreducible factors of degree e correspond to Puiseux orbits of length e —
i.e., **meridian-orbit structure = C((ε))-factorization type**. (Residue-field
bookkeeping, per audit: at the generic point of D the residue field is C(D),
and a boundary divisor can carry nontrivial residue degree over D — as an S₂
boundary component mapping 2:1 indeed does. After base change to a geometric
generic point the residue extensions split, and each geometric Puiseux orbit
has length equal to its ramification index; the e–f bookkeeping below is in
that geometric sense.) Converging
sheets are points of the source part; escaping orbits are boundary points of
Y. Hence, over generic points of D:

- a T-component has one boundary point with e = 2 (tame): different exponent
  e − 1 = 1;
- S₁ has one unramified boundary point (e = 1, degree 1 over D);
- S₂ has unramified boundary of total degree 2 over D (one divisor mapping
  2:1, or two mapping 1:1).

The reduced intrinsic branch cycle (pushforward of the different, reduced) is

**Br(F) = [S_T]** — silent boundary contributes zero, by construction of the
different, not by a coordinate choice.

Fable check: the coordinate discriminant is disc_x(M) = −4H²·S̃. Per audit,
the identification of H² as the conductor/index divisor is NOT claimed: **H²
is an extraneous square factor arising from the nonintegral/nonprimitive
monogenic presentation by x** (x fails to separate two sheets over H — proven
at (−8/27,0,1)); its precise index-ideal interpretation remains to be
computed by an integral-closure calculation in codimension one. The reduced
intrinsic branch Br(Fable) = [S_F] is derived independently of this, from the
e = 2 tame boundary structure (Puiseux–ramification bridge). The exact
escaping branch at (B,C) = (4,0) — x = i/(2s), u = i/(2s) − ½ + …,
y = 1 + 3is + O(s³), z = 6is − 26s² + … with ε = s² — meets the boundary
divisor transversally: ν*(dε) = 2s ds, different exponent 1 = e−1. ✓

## Gate 3: The silent-cycle identity (theorem-grade given Gates 1–2)

Define the codimension-one defect cycle Def⁽¹⁾(F) = Σ_D δ_D[D]. By Gate 1:

**Def⁽¹⁾(F) = 2[S_T] + [S₁] + 2[S₂],  Br(F) = [S_T],**

**Σ_silent(F) := Def⁽¹⁾(F) − 2Br(F) = [S₁] + 2[S₂].**

The Fable pattern is exactly **Σ_silent(F) = 0**. The pairing resolves the
complementary blindness (verified on all three model rows):

| | T | S₁ | S₂ |
|---|---|---|---|
| defect cycle | 2 | 1 | 2 |
| branch cycle | 1 | 0 | 0 |
| silent cycle | 0 | 1 | 2 |

**Numerical consequences.** With s = deg S_F, t = deg S_T, Δ = defect-degree
(Gate 4 of the ledger): Δ = 2t + deg S₁ + 2 deg S₂ and s = t + deg S₁ + deg S₂
give

**deg S₁ = 2s − Δ,  deg S₂ = Δ − s − t,  s + t ≤ Δ ≤ 2s.**

Fable: (s, t, Δ) = (4, 4, 8) ⇒ deg S₁ = deg S₂ = 0: its silence is recovered
from three intersection-theoretic degrees alone. The admissible
silent-bearing configurations at small degree are enumerated in the script;
the minimal cubic candidate is **(s, t, Δ) = (2, 1, 3): one T-line plus one
S₁-line** — the first configuration Gate 4 must kill or realize.

## Gate 4: Translation into Cl(Y) and K_Y (the pressure point)

Y is normal, U = C³_source ≅ A³ open with divisorial boundary B = ∪B_i.

**(i) Cl(Y) is freely generated by the boundary divisors.** The excision
sequence Z^{#B_i} → Cl(Y) → Cl(U) = 0 is exact, and the kernel of the first
map consists of divisors of functions invertible on U; O(A³)^× = C^×, so the
map is injective: **Cl(Y) ≅ ⊕_i Z[B_i]**. (Theorem-grade.)

**(ii) K_Y = R_ν, supported on the transposition boundary only.** The
ramification formula for the finite ν of normal varieties (char 0, tame in
codim 1) gives K_Y = ν*K_{A³} + R_ν = R_ν = Σ(e_i − 1)[B_i] = [B_T].
(Theorem-grade in codim 1.)

**(iii) The Keller condition as a valuation identity.** The form
ν*(dA∧dB∧dC) restricts on U to det J_F · dx∧dy∧dz = −2·dx∧dy∧dz — nowhere
zero. Its divisor on Y is R_ν. Hence for EVERY boundary divisor:

**v_{B_i}(dx∧dy∧dz) = e_i − 1.**

A T-divisor is a volume-form zero of order 1; a **silent divisor is a
volume-form-NEUTRAL divisor at infinity of A³: v_{B₀}(dx∧dy∧dz) = 0** —
neither zero nor pole of the affine volume form across a divisor that the
source never meets.

**The sharp question (reviewer's formulation, adopted verbatim as the
target):** can a finite normal cubic cover Y → A³ contain a generically
unramified boundary divisor while its complement is itself A³, its
function-field monodromy is S₃, and its relative canonical class is supported
only on the transposition boundary?

Three observations that calibrate its difficulty:

1. Volume-neutral divisorial valuations at infinity of Aⁿ DO exist for n ≥ 2
   (e.g., in A², the third infinitely-near blowup over the line at infinity
   reaches v(dx∧dy) = 0; in A¹ none exist: v(dx) = −2 at infinity — the
   dimension-1 silent exclusion is exactly triviality of étale self-maps of
   A¹). So the question is not killed by valuation theory alone: the tension
   must come from B₀ simultaneously (a) being volume-neutral, (b) finitely
   covering an affine uniruled hypersurface D (birationally for S₁, 2:1 for
   S₂), (c) sitting on Y with Cl(Y) free on boundary and K_Y = [B_T].
2. The 2D shadow: Orevkov's silent cases (his partitions 1+1 and 1+1_jump)
   are precisely the plane instances of this question, and they die — the
   class-group/canonical translation of his cases is the statement that no
   volume-neutral boundary divisor exists for plane cubic covers. The 3D
   question is its genuine generalization, and it is open.
3. For S₁-components the boundary divisor is BIRATIONAL to D, hence a
   uniruled affine-covering surface. Per audit: adjunction on B₀ is NOT yet
   available — it requires hypotheses not established here (B₀ normal or
   suitably Cohen–Macaulay; the relevant divisors Cartier or Q-Cartier), and
   Cl(Y) ≅ ⊕Z[B_i] does NOT make the B_i Cartier. The adjunction computation
   is a genuine future research project, not a verification gate.

## Status

Gate 1: theorem-grade on the existing lemma stack. Gate 2: upgraded to
theorem-grade via the Puiseux–ramification bridge (Newton–Puiseux =
C((ε))-ramification; ZMT factorization; different in codim 1); the Fable
instantiation is exact. Gate 3: theorem-grade given 1–2; numerical identities
verified, Fable silence recovered as (deg S₁, deg S₂) = (0,0) from (4,4,8).
Gate 4: (i)–(iii) theorem-grade; the silent-exclusion question itself is
open and is the designated frontier. All micro-models verified (T: disc odd;
S₁: disc order 0; S₂: disc = perfect square, defect 2, trivial meridian —
the disc-blind defect-2 impostor that makes the Def/Br pairing necessary).
No priority claims; Jelonek's structure theory cited for S_F; the underlying
map remains subject to community verification.

**Final-audit repairs applied (this version):** (1) residue-degree wording
corrected to the geometric-generic-point formulation; (2) the H²-as-conductor
identification downgraded to "extraneous square factor, index-ideal
interpretation open"; (3) the adjunction step reclassified from next gate to
future research (Cartier/normality hypotheses unestablished). This document
is frozen as Paper II material.
