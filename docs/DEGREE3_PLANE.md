# Orevkov's cubic plane theorem in ledger–monodromy form
(per the reviewer's identification: the two-front decomposition IS Orevkov's
1987 proof translated into Jelonek–monodromy–ledger language. Machine
verifications in `degree3_plane.py`. Attribution: **the theorem is Orevkov's**;
the contribution here is the shorter structural explanation and the
mechanized micro-obstructions.)

**Theorem (Orevkov, 1987).** There is no noninvertible Keller map
F: C² → C² of generic degree 3.

## 1. Dictionary lemma

Orevkov compactifies, resolves at infinity, and accounts multiplicities along
dicritical components; his central identity

Σ_{l ⊂ L_F} [ μ_l + Σ_{x ∈ π(l)∖{∞}} (μ_x − μ_l) ] = N − 1

is a **non-properness budget**. The dictionary: **μ_l equals the generic
meridian-orbit length of the escaping branch at the dicritical component l.**
Micro-models (verified):

- orbit length 1 (silent): escaping root with INTEGRAL pole order
  (M = εx³ + x² + …: big root ~ −1/ε); the discriminant is generically
  NONVANISHING along the divisor (disc|_{ε=0} = 1−4c ≠ 0) — silent branches
  are invisible to disc, matching trivial meridian action;
- orbit length 2 (transposition): the Fable normal form M = εx³ + 4x − 2c;
  roots ±(i/2)ε^{−1/2}, half-integer order, swapped by the meridian; disc =
  −4ε(27c²ε + 64) vanishes to ODD order 1.

Orbits of *converging* sheets are impossible (L2 uniformity + étale
no-merge), so all orbit content lives on escaping branches: μ-accounting and
meridian-orbit accounting agree. (Caveat kept explicit: Orevkov's identity is
an at-infinity resolution statement; our affine χ-ledger χ(T) = dχ(S) − (d−1)
is its affine shadow; they agree on the case list below, and no claim is made
that one formally derives the other.)

## 2. Cubic ledger theorem

For d = 3 the budget is N − 1 = 2, with exactly three partitions:

| partition | configuration |
|---|---|
| 1 + 1 | two silent escape branches |
| 1 + 1_jump | one silent branch + exceptional point jump |
| 2 | one transposition orbit |

These are precisely Orevkov's three cases.

## 3. Silent-front theorem

In partitions 1+1 and 1+1_jump, every escaping branch has orbit length 1, and
converging sheets are always fixed (L2); hence **every divisorial meridian is
the identity**. Meridians normally generate π₁ of the complement, so the
monodromy is trivial and the connected 3-sheeted cover is trivial —
disconnected total space over a connected base: contradiction. (This is the
ledger-monodromy form of Orevkov's statement that these cases would yield a
connected unbranched 3-sheeted cover of C² or C²∖{p}, both simply connected.)

**Cubic plane silent-divisor exclusion.** A 3-sheeted Keller map C² → C²
cannot have an identity-monodromy divisorial component. *(Degree-specific;
NOT the universal silent-divisor lemma, which remains open in general.)*

## 4. Transposition-front theorem

Partition 2 = 2 exhausts the budget on a single length-2 orbit: S_F is
irreducible with transposition meridian and generic fiber 1. **Imported heavy
step (Orevkov):** the dicritical component maps biregularly onto a nonsingular
affine curve; budget-exhaustion gloss: any singularity or non-injectivity
would create multiplicity jumps μ_x > μ_l, overspending N−1. So S_F ≅ A¹,
smooth and embedded; **Abhyankar–Moh** straightens it to a coordinate line.
Then

π₁(C² ∖ A¹) ≅ Z,

and a connected triple cover needs a transitive image of Z in S₃ — i.e. a
3-cycle generator. But the generator IS the meridian, and the meridian is a
transposition. ⟨(12)⟩ is not transitive on three sheets: contradiction. ∎

**Summary mechanism.** *A cubic plane counterexample has only two possible
mechanisms. Silent escape cannot maintain a connected cover; transposition
escape makes the bad curve too topologically simple to support S₃.*

## 5. Complementary H₁-obstruction lemma (machine-verified)

Independently of the biregularity import: suppose the transposition
configuration had an irreducible SINGULAR bad curve of trefoil type
(π₁(C²∖S) ≅ B₃ = ⟨a,b | aba = bab⟩ — e.g. the cuspidal discriminant cubic).
Any surjection B₃ ↠ S₃ sends meridians (all conjugate) to transpositions
(conjugate 3-cycles only generate A₃). The source complement C²∖T, with T
irreducible (forced: every component of T = V(g∘F) dominates S; generic fiber
1 ⇒ one component), must have H₁ = Z. But Reidemeister–Schreier on the
index-3 subgroup gives relator matrix [[−1,0,1,0],[1,1,−1,−1],[−1,0,1,0]] with
Smith form diag(1,1,0,0):

**H₁(index-3 subgroup of B₃) = Z² ≠ Z. Contradiction.**

So the cuspidal candidate dies at the H₁ level, with no resolution at
infinity. Under the budget theorem this configuration never arises (S must be
smooth A¹); the lemma is the belt-and-suspenders closure — and the method
(RS + Smith vs. free H₁ of curve complements + forced component counts)
exports to dimensions where no biregularity theorem exists.

## 6. The tautological cubic-resolvent model (the negative control)

G(t,p) = (p, −t³ − tp) on the graph {q = −t³ − pt} ≅ C²: a genuine degree-3
polynomial self-map of C² realizing the B₃ covering data over the
discriminant cuspidal cubic K = {4p³ + 27q² = 0}. Verified: det J = 3t² + p —
nonconstant, vanishing exactly on the critical parabola whose image is K;
fibers 2 / 1 over K∖{0} / cusp (sheets MERGE at the branch — the move
étaleness forbids); Euler ledger balanced (1 = 3(1−1) + 1). The Keller version
would delete the critical curve (escape instead of merge), fiber 1 over K,
χ(T) = 3χ(K) − 2 = 1 — all consistent as covering topology. **Everything soft
exists; only det J = const is obstructed.** The obstruction to a cubic plane
counterexample is genuinely algebraic, exactly where Orevkov's resolution
machinery operates.

## 7. Why the Fable map escapes in dimension three

The fixed-sheet ledger survives in all dimensions. The step that fails in the
plane proof is:

transposition divisor ⟹ S_F ≅ A¹ ⟹ π₁(C²∖S_F) ≅ Z.

In C³ the bad set is a **singular quartic surface** (cuspidal edge Γ, missed
locus of codim 2), and its complement carries π₁ ↠ S₃ — full nonabelian
monodromy. The Fable map realizes exactly the first topology the plane
argument cannot collapse: degree 3, S₃ global group, transposition meridian,
fiber trichotomy 3/1/0 on C³∖S_F, S_F∖Γ, Γ — every plane-forced collapse
evaded by one extra dimension of room in the bad set.

## 8. Status and open exports

- The theorem and its proof are **Orevkov's (1987)**; Domrina–Orevkov extend
  to 4 sheets; the 5-sheeted exotic covering marks where covering topology
  stops sufficing. No priority claimed on any exclusion.
- Candidate contributions: the dictionary + budget-as-ledger presentation;
  the silent-front kill via L2/meridian-generation (short); the H₁-obstruction
  lemma (mechanized; biregularity-free); the tautological-model localization
  of the obstruction; the precise diagnosis of the 3D escape.
- Open: the universal silent-divisor lemma (all d, all n); a 3D budget
  identity playing the role of Orevkov's at-infinity accounting (the affine
  shadow 2χ(S_F) + χ(Γ) = 2 checks on the Fable map: 2·1 + 0 = 2); and the
  d = 4, 5 plane cases in this language.
