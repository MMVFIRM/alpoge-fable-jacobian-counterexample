# GeoVerify → Conjecture Tester: what I built and what it found

## 1. What GeoVerify actually is (measured, not claimed)

GeoVerify is an **expression-equivalence checker** — a grader that decides
whether two mathematical expressions are the same. I reproduced its full
benchmark:

| Suite | Result |
|---|---|
| 27-case unit suite | **24/27 = 88.9%** |
| 170-instance benchmark | **90.6%** (precision 96.9%, recall 81.6%, F1 88.6%) |

This is a real, working grader that beats naive string matching — but it is
**not** the 95%+ its comparison table implies, and it has genuine failure modes:

- Read `x(x-1)` as a **function call**, not multiplication → called `x³−x` and
  `x(x−1)(x+1)` *non-equivalent* at 0.85 confidence (a confident wrong answer).
- **Dropped subscripts** → called `ε₀` and `ε₂` equal.
- **Dropped integral bounds** → called `∫₀^∞` and `∫₂^∞` equal.
- **Real-positive-only** numeric sampling → blind to failures off the positive reals.

(Several of the benchmark's own "errors" are mislabeled cases from buggy
perturbation generators — e.g. it calls `2mω²` and `2ωm²` equivalent. So the
true accuracy is fuzzy in both directions.)

## 2. What a grader can and cannot do for conjectures

GeoVerify checks "answer == reference." It does not search, construct, or check
proof validity. **No setting of its dials makes a proof pop out.** The right role
for a verifier is the *check* half of a **generate-and-verify loop**: a generator
proposes candidate objects; a cheap, exact verifier checks each one. This can
**refute** conjectures (a counterexample is a finite, checkable object). It
essentially never **proves** a universal statement.

Note: even the Jacobian counterexample was verified by a *purpose-built* SymPy
check (compute the Jacobian determinant; check three points collide), **not** by
GeoVerify. So I generalized that into a reusable harness.

## 3. The harness: `conjecture_tester.py`

Works on SymPy objects (sidestepping the fragile LaTeX path) and adds:

- `prove_or_refute_identity` — symbolic first, then **complex-plane** sampling
  (fixes GeoVerify's real-only blind spot).
- `check_candidate(hyp, concl)` — is this object a counterexample? (Jacobian pattern, generalized)
- `search_counterexample(space, pred)` — iterate a space, return the first witness.
- `test_jacobian_counterexample` — constant-nonzero Jacobian **and** non-injective.
- Diophantine helpers (`is_perfect_power`, etc.).

Every verdict carries the method and a **concrete witness** you can re-check.

## 4. Validation on known-answer cases (all pass)

- **Fixed the case GeoVerify blew:** `x³−x = x(x−1)(x+1)` → *identity*.
- **Complex blind spot fixed:** `√(x²) = x` → *refuted*, witness `x ≈ −0.50 − 2.94i`.
- **Jacobian counterexample re-verified through the tool:** Jacobian det = −2
  (constant, nonzero) and the three points collide → *counterexample* confirmed.
- **Rediscovered a real, once-open counterexample from scratch** (search, 3.5 s):
  Euler's sum-of-powers conjecture, n = 5, was open 1769–1966. The tool found
  **27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵** (Lander–Parkin, 1966) — four fifth powers
  summing to a fifth power, which Euler said was impossible.

## 5. Applied to an OPEN conjecture: Erdős–Straus (1948)

Claim: for every integer n ≥ 2, `4/n = 1/x + 1/y + 1/z` in positive integers.

Reasoning used to shrink the search (this is the "reason, then check" part):
1. **Multiplicativity** → only **primes** need checking.
2. Standard identities cover every residue class mod 840 **except** the six
   classes `{1, 121, 169, 289, 361, 529}` → only "hard-residue" primes matter.

Tool result: **verified for all hard-residue primes up to 10⁷** (20,513 primes,
50 s) — every one has an explicit `(x, y, z)`. **No counterexample.**

### Honest scope

This is **not** progress on the open problem. The literature has verified
Erdős–Straus past 10¹⁷; my 10⁷ just demonstrates the harness reproduces known
verification and would flag a counterexample if one appeared. Refuting the
conjecture needs a single n with no decomposition; proving it needs an idea no
search can supply. The tool is a genuine, reusable counterexample-hunter and
identity-checker — it is not, and cannot be, a proof oracle for open problems.
