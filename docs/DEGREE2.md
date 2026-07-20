# Galois exclusion, degree-2, and conditional degree-minimality
(v3 — incorporating the full referee report; machine instantiations in
`degree2.py`; builds on the proof-grade stratification of `STRATA.md`)

## 0. Degree conventions

For dominant polynomial F: Cⁿ → Cⁿ: **coordinate degree** (max total degree of
components; Fable: (7,6,4); Wang's theorem lives here), **field-extension
degree** [C(x₁..xₙ):C(F₁..Fₙ)], and **topological/geometric degree** (generic
fiber cardinality). In characteristic 0 the latter two coincide; everything
below concerns this common value d. Fable: M irreducible over C(A,B,C) and
generic fiber 3 ⇒ d = 3, prime.

## 1. History and novelty ledger (corrected)

**Campbell's theorem** (1973, Math. Ann.): a Keller map whose function-field
extension is Galois is invertible. **Degree-2 exclusion in every dimension is
classical**: quadratic extensions in characteristic 0 are automatically
Galois. The 2024 prime-degree manuscript itself records the Galois-case origin
of the degree-2 exclusion.

**Campbell's own proof was not merely field-theoretic**: per Byrnes–Lindquist,
he realized the Galois group by covering transformations and used the topology
(simple connectivity) of the relevant complement. The correct novelty claim is
therefore NOT "first geometric proof" but:

> a **Jelonek-set, local-monodromy, divisor-theoretic** proof of Campbell's
> theorem, locating the obstruction at surviving sheets over the
> non-properness divisor.

The fixed-sheet/principal-divisor formulation was not found in the literature
checked so far, but a genuine novelty claim requires careful comparison with
Campbell, Abhyankar, Razar, Wright, Oda, Byrnes–Lindquist, and later
topological treatments. Until then: candidate-new proof route; classical
theorem.

## 2. The lemmas

F Keller (det J_F ∈ C^×, étale), dominant, degree d ≥ 2; S = S_F its Jelonek
set — empty or a hypersurface for a dominant generically-finite polynomial map
(Jelonek); F is a proper étale d-cover over U = Cⁿ∖S.

- **L0 (étale fiber bound):** every fiber has ≤ d points; fibers over S have
  ≤ d−1. [Open-image + escape argument.]
- **L1 (meridians):** if S = ∅ the cover of the simply connected Cⁿ is
  trivial, d = 1. Otherwise meridians normally generate π₁(U); a connected
  nontrivial cover forces SOME meridian to act nontrivially. *(L1 does NOT
  say the meridian around every component is nontrivial — see §4.)*
- **L2 (orbit uniformity):** at a generic transverse disc to a divisorial
  component, any bounded sheet extends through the center and is individually
  fixed; hence every nontrivial monodromy orbit escapes uniformly (merging is
  banned by étale local injectivity). The generic fiber over the component is
  the set of converging fixed sheets. *(An identity meridian may coexist with
  an escaping single-valued branch of integral pole order.)*
- **L3 (no generically missed divisor — fully algebraic form):** for an
  irreducible divisor D = V(g) ⊆ S: F⁻¹(D) = V(g∘F); dominance makes g∘F
  nonconstant, so V(g∘F) is a nonempty hypersurface; for any irreducible
  component E, F|_E is quasi-finite (F étale), so dim cl(F(E)) = dim E = n−1;
  cl(F(E)) ⊆ D irreducible of dimension n−1 forces cl(F(E)) = D. Generic
  points of D have preimages. ∎
- **Fixed-sheet corollary:** every nontrivial meridian permutation must fix at
  least one converging sheet; consequently no divisorial component is
  generically omitted, and missed sets of counterexamples have codim ≥ 2.

## 3. Theorem A (Campbell's theorem; Jelonek–monodromy–divisor proof)

*If a Keller map's extension C(x₁..xₙ)/C(F₁..Fₙ) is Galois, F is a polynomial
automorphism.*

*Proof.* Suppose d ≥ 2. S = ∅ gives a trivial cover of Cⁿ, d = 1: contra.
So S ≠ ∅ is a hypersurface. Galois-ness ⟺ monodromy acts regularly on the
generic fiber; every nonidentity element is then fixed-point-free. By L1 some
meridian is nontrivial, hence fixed-point-free; by L2 all its orbits escape,
so its component is generically omitted; L3 forbids this. Hence d = 1.

**Endgame (corrected):** d = 1 ⇒ F birational and quasi-finite ⇒ open
immersion (Zariski's Main Theorem) ⇒ injective ⇒ **surjective by
Ax–Grothendieck / Białynicki-Birula–Rosenlicht** (an injective polynomial
endomorphism of Cⁿ is surjective) ⇒ automorphism. ∎

**Corollary B (degree-2 exclusion — classical).** No Keller map has d = 2;
every Keller map with d ≤ 2 is an automorphism.

## 4. Degree-three structural constraint (corrected — Correction 1)

For a degree-3 counterexample:

- Global monodromy is full S₃ (A₃ is regular: excluded by Theorem A).
- **Every divisorial meridian is the identity or a transposition; at least one
  is a transposition; every NONTRIVIAL divisorial meridian is a
  transposition** (3-cycles are fixed-point-free: banned by the corollary).
- Over a transposition component: generic fiber exactly 1.
- Over an identity-monodromy component: generic fiber **1 or 2** — the
  stronger universal claim of v2 is withdrawn. Recovering it would require the
  presently-unsupplied lemma:
  **(Open) Silent-divisor lemma:** D ⊆ S_F ⇒ the generic meridian around D is
  nontrivial. *Not automatic for non-proper coverings; an identity meridian
  with one single-valued escaping branch (integral pole order) is locally
  consistent. In dimension 2 this is plausibly where Orevkov-type constraints
  act.*

**Map-specific result (Fable): its unique bad divisor IS transposition-type —
exactly, not numerically.** S_F(Fable) is irreducible; at its generic point
H ≠ 0 (H ∩ S_F = Γ, codim 2, `strata.py`), so disc_x(M) = −4H²S̃ vanishes to
FIRST order across S_F; a meridian loop reverses √disc, so the meridian acts
by an odd permutation of the three sheets — a transposition. This upgrades the
numerical monodromy loop ([1,0,2]) to an exact statement and confirms the
Fable map has no identity-monodromy (silent) divisor. Fiber 1 on S_F∖Γ then
re-derives the stratification's U₁ count from pure monodromy.

## 5. Conditional Degree-Minimality Theorem (retitled — per report)

Classical fact: **every Keller counterexample has generic degree ≥ 3**
(degree 2 is automatically Galois; Galois Keller maps are invertible).

**Conditional theorem.** *If the Alpöge–Fable map is a noninvertible Keller
map of generic degree 3 — as every machine verification in this project
indicates, pending external verification — then it has the minimum possible
generic degree of any counterexample to the Jacobian Conjecture.* It is
non-Galois of the first degree at which non-Galois extensions exist: the exact
boundary of the automatic-Galois obstruction, with all forced degree-3
structure (S₃ monodromy, transposition meridian on its unique divisor, fiber
1 generically on S_F, missed set of codim 2) realized and verified.

**Prime-degree remark (softened — per report).** arXiv 2407.13795 (v1, July
2024; no refereed publication found) claims no 2D Keller map has prime
function-field degree. If the Fable map survives verification, it disproves
any unrestricted extension of that exclusion from dimension 2 to all
dimensions — the claim is conditional on the candidate map, and is so stated.

## 6. Mechanism instantiations (exact; script)

- (B,C) = (4,0) line: M(x; 1+ε, 4, 0) = 4x(4εx² + 1); fixed sheet x = 0
  converges to (0,4,−63); 2-orbit ±(i/2)ε^{−1/2} swaps and escapes. L2 and
  the fixed-sheet corollary in closed form.
- Negative control G(x,y) = (x²,y): det J = 2x; swap monodromy resolved by
  merging on {det J = 0} — the move étaleness forbids.

## 7. Honest scope

Theorem A is Campbell's theorem; the proof route is candidate-new pending the
literature comparison listed in §1. Corollary B classical. §4's universal
degree-3 claims are only what the lemmas support; the silent-divisor lemma is
explicitly open. §5 is conditional on external verification of the map. The
endgame now cites Ax–Grothendieck/BBR where v2 leaned on ZMT alone.
