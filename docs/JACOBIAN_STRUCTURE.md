# Dissecting the Alpöge–Fable Jacobian counterexample (computed 2026-07-20)

The map (posted 2026-07-19, verified in this session):
F(x,y,z) = ( u³z + y²u(4+3s),  y + 3xu²z + 3xy²(4+3s),  2x − 3x²y − x³z ),
with s = xy, u = 1+s. det J = −2 everywhere; three distinct points share the
image (−1/4, 0, 0).

All results below are computed and verified in `structure.py` / `twod.py`.

## 1. The map factors through a single "potential"

Define W = u²z + y²(4+3s). Then, as exact polynomial identities:

- F₁ = u·W
- F₂ = y + 3x·W
- u²·F₃ = x(2+s) − x³·W

The whole map is built from one scalar potential W and the unit u = 1+xy.
Crucially, **z enters only through W, and linearly** — z is the "free direction"
that lets fibers escape to infinity (see §3).

## 2. The map is generically 3-to-1 (topological degree 3)

Eliminating via the identities reduces the fiber F = (A,B,C) to two equations in
(x, u): u² − u(1+xB) + 3x²A = 0 and u³C − xu(1+u) + x³A = 0. The resultant in u
has degree 6 in x; at five independent random targets, exactly **3 preimages**
survive verification (residuals ≈ 1e−16), cross-validated once by an exact
Gröbner solve (also 3). The famous collision point (−1/4,0,0) is a *generic*
point of the map — its 3 preimages are the full fiber.

## 3. Non-properness is forced, and we located it

Since det J = −2 ≠ 0 everywhere, F is étale: fibers can never merge. But C³ is
simply connected, so a *proper* finite étale self-cover would have to be an
isomorphism. Hence any counterexample **must** be non-proper: where the fiber
count drops, preimages escape to infinity. Computation confirms: the elimination
degenerates exactly on {A = 0}, and there fibers genuinely drop —
F = (0,0,1) has exactly **1** preimage (x=1/2, y=0, z=0, exact), while
F = (0,1/2,−3) still has 3. No missed value was found: every tested target,
including on the degenerate locus, has a preimage — consistent with F being a
surjective, generically-3:1, non-proper étale self-map of C³.

## 4. Rigidity: the coefficients (4,3) are forced

Generalizing to g(s) = a+bs and F₃ = αx + βx²y + γx³z, imposing det J = const
and solving the 12 coefficient equations exactly gives ONLY:
- degenerate branches (det = 0), and
- **a = 4, b = 3, α = −2γ, β = 3γ, det = 2γ** — i.e. the original map with F₃
  rescaled, which is just diag(1,1,γ′)∘F.

So within this ansatz the counterexample is **rigid**: no genuine deformation
family; (4,3) is the unique working coefficient pair. (The "new member" the
harness verified is linearly equivalent to the original — reported as such.)

## 5. The mechanism has no low-degree 2D analogue

The natural 2D transfer is F = (u·W(x,y), y + λx·W(x,y)). Imposing det J = const
exactly, for ALL polynomial W of total degree ≤ 4 (15 coefficients, 52
equations): every solution branch forces **W = 0** (degenerate). Verified:
**no nontrivial 2D analogue with deg W ≤ 4**; degrees 5–6 timed out (open here).
Structural reading: in 3D, W is linear in the spare variable z — the escape
direction §3 requires; in 2D there is no spare variable. Consistent context:
the 2D Jacobian Conjecture remains open and is verified for degree ≤ ~100
(Moh 1983; pushed to 108 in 2022), so nothing low-degree could exist anyway.

## Honest scope

These are machine-verified computations about a 24-hour-old object, not claimed
theorems of record; the professional community is certainly running similar
analyses in parallel, and no priority is claimed. The generic-fiber and rigidity
computations are exact (symbolic elimination / Gröbner); preimage lifts are
numeric but verified to ~1e−16 and spot-checked exactly.
