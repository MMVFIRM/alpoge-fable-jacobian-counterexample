# Paper II index — structural consequences (HELD until Paper I survives outside verification)

Each document lives in `docs/`, with verifying scripts in `scripts/`.
Rigor labels: [T] theorem-grade on the package's lemma stack; [D] dictionary-
grade (proved at branch level, some global step imported or sketched);
[O] open question, precisely posed.

1. **JACOBIAN_STRUCTURE.md** — potential W, generic 3:1, rigidity of the
   coefficients (4,3), no low-degree 2D analogue of the mechanism. [T]
2. **JELONEK_GALOIS.md** — Jelonek surface, fiber cubic, S₃, monodromy.
   (Superseded in part by STRATA.md; kept for the record.) [T with noted
   supersessions]
3. **LEDGER.md** — exact image C³∖Γ, Euler-characteristic ledger, 2D slice
   demonstration χ(X) = 4. [T]
4. **STRATA.md** — proof-grade 3/1/0 stratification: master identity,
   saturation gate, explicit sections, H-locus resolution. [T]
5. **DEGREE2.md** — Campbell's theorem via Jelonek–monodromy–divisor;
   degree-2 exclusion (classical); Conditional Degree-Minimality Theorem:
   the Fable map attains the minimum possible generic degree 3. [T; theorem
   classical, route candidate-new pending literature comparison]
6. **DEGREE3_PLANE.md** — Orevkov's cubic plane theorem in ledger–monodromy
   form; H₁-obstruction lemma (Reidemeister–Schreier, machine-verified);
   tautological cubic-resolvent negative control. [T for the translation;
   Orevkov's biregularity imported at the marked step]
7. **DEFECT_LEDGER_3D.md** — constructible defect ledger ∫δ dχ_c = d−1
   (all dimensions); divisorial dictionary; jump strata; sliced defect class
   δ̂(Fable) = (0, 8, −1, 2). [Gate 1 T; Gate 2 D; Gates 3–4 T for the
   instantiations]
8. **CUBIC_3D_SILENT_CYCLE.md** — T/S₁/S₂ trichotomy; Σ_silent = Def⁽¹⁾ − 2Br
   = [S₁] + 2[S₂]; degree identities (Fable: (4,4,8) ⇒ silent degrees 0);
   Cl(Y)/K_Y translation; volume-neutrality formulation of the open
   silent-divisor question. [Gates 1–3 T (Gate 2 via the Puiseux–ramification
   bridge, geometric-generic-point bookkeeping per audit); Gate 4 identities
   T, question O]

Final-audit repairs applied to item 8 before freezing: (i) residue-degree
wording (geometric generic point); (ii) H² identified only as an extraneous
square factor of the monogenic presentation — index-ideal interpretation
open; (iii) adjunction on silent boundary reclassified as future research
(Cartier/normality hypotheses not established; Cl(Y) free does not make
boundary divisors Cartier).

Explicitly open problems carried by Paper II: the universal silent-divisor
lemma; the index-ideal computation for H; the adjunction program on Y; a 3D
analogue of Orevkov's at-infinity budget identity beyond the affine shadow.
