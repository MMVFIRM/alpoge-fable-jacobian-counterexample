# The Jelonek set and Galois structure of the Alpöge–Fable map
(computed & machine-verified 2026-07-20; scripts: `jelonek.py`)

Continuing from `JACOBIAN_STRUCTURE.md`: F is étale (det J = −2), generically
3:1, and — because C³ is simply connected — necessarily non-proper. Here we
compute *exactly* where and how properness fails, and what the cover's
symmetry is.

## 1. The Jelonek set, exactly

Escapes to infinity with bounded image go x → ∞, y → v ≠ 0, forcing
B = v + 3A/v and C = (4v−B)/(3v²). Eliminating v:

**S_F : 27A²C² − 18ABC + 16A + B³C − B² = 0**

an irreducible quartic surface, rationally parametrized by (A, v) — hence
uniruled, exactly as Jelonek's general theorem demands. Checks: on {A=0} it
degenerates to B²(BC−1) — precisely the two fiber-drop curves found earlier;
the collision point (−1/4, 0, 0) gives S = −4 ≠ 0, so it is *not* in S_F
(consistent with its full 3-point fiber). Sing(S_F) is the rational curve
A = 4/(27C²), B = 4/(3C).

## 2. The minimal polynomial of the cover — a depressed cubic

Factoring the fiber resultant gives R = A·x³·M (first factors spurious) with

**M(x; A,B,C) = S̃·x³ + (4 − 3BC)·x − 2C**,  S̃ = the S_F polynomial.

The x-coordinates of the fiber over (A,B,C) are exactly the roots of M. Two
immediate exact corollaries:

- **The leading coefficient of the fiber polynomial IS the Jelonek equation.**
  Sheets escape to infinity precisely where the cubic drops degree — the
  cleanest possible mechanism for non-properness.
- **M is depressed (no x² term): the three preimages of ANY point have
  x-coordinates summing to zero.** Check on the famous collision fiber:
  0 + 1 + (−1) = 0. Indeed M at (−1/4,0,0) is −4x(x−1)(x+1), roots {−1,0,1} —
  the exact collision x-coordinates.

Because M has no x² term, when S̃ → 0 *two* roots escape simultaneously
(±√(−p/S̃)) — so the fiber over any point of S_F has exactly **one** finite
point, not two. Verified exactly: fiber over (1,4,0) ∈ S_F is the single point
(0, 4, −63); control point (1,4,1/10) off S_F has 3.

Fiber stratification (all exact): 3 preimages off S_F; 1 on S_F.

## 3. Galois group = S₃; the closure branches exactly over S_F

disc_x(M) = −4·(27AC² − 9BC + 8)² · S̃.

The discriminant is a perfect square times S̃ to the **first** power — not a
square in C(A,B,C). Therefore:

- the Galois group of the degree-3 extension C(A,B,C) ⊂ C(x,y,z) is the full
  **S₃**, not Z/3: the Alpöge–Fable map is a **non-Galois triple cover**;
- its Galois closure is a 6:1 cover **branched exactly over the Jelonek set**
  (the odd-exponent factor of the discriminant *equals* the S_F equation);
- since disc winds once around {S̃=0}, the monodromy of a meridian loop around
  S_F must be an odd permutation — i.e. a **transposition**: the two escaping
  sheets swap; the surviving sheet is fixed. (This is exact, forced by the
  odd exponent; a 400-step numerical continuation loop confirms it: permutation
  [1,0,2].)

## 4. Topological corollary

The permutation representation π₁(C³ ∖ S_F) → S₃ is transitive (the source of
F is connected) and sends meridians to transpositions; the normal closure of a
transposition is all of S₃. Hence **π₁(C³ ∖ S_F) surjects onto S₃ — the
complement of this quartic surface has nonabelian fundamental group**, and the
Alpöge–Fable map restricted off its bad set is precisely the degree-3
non-Galois covering realizing it. (The singular curve of S_F is what permits
nonabelian π₁, in the spirit of Zariski's theory.)

## 5. Honest scope

Exact: S_F's equation and parametrization, the factorization R = A·x³·M, the
discriminant identity, the fiber counts at the quoted points, the S₃/branching
conclusions, the sum-zero corollary. Informal-but-covered: exhaustiveness of
escape channels (x-escapes are governed *exactly* by M's leading coefficient;
the x-bounded channels were analyzed and close off — a formal proof would
organize this via Newton polygons at infinity). Numerical: only the monodromy
loop, and its conclusion is independently forced by the discriminant parity.
This is a 24-hour-old object; parallel work by the community is certain and no
priority is claimed.

## 6. Where this points

Any étale JC-counterexample in any dimension must repeat this template: a
non-proper cover whose fiber polynomial degenerates over a uniruled Jelonek
hypersurface, with monodromy rich enough to keep the total space connected.
In dimension 2 the Jelonek set would be a plane curve and the same machinery
(fiber polynomial, discriminant parity, π₁ of the curve complement, Euler
characteristic bookkeeping χ(C²∖F⁻¹(S)) = d·χ(C²∖S)) becomes a concrete
obstruction program — a *proof-shaped* attack on the still-open 2D case,
rather than a search.
