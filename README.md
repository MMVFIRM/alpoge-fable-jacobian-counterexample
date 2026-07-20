# The Alpöge–Fable Map

## An independently checkable claimed counterexample to the Jacobian Conjecture in dimension 3

> **Current status:** This repository presents a claimed counterexample whose central certificate consists of two finite, exact symbolic computations. The package has been frozen for independent review. The computations are reproducible; the broader mathematical community has not yet completed external verification.

The Jacobian Conjecture asks whether a polynomial map

\[
F:\mathbb C^n\to\mathbb C^n
\]

with a nonzero constant Jacobian determinant must always have a polynomial inverse.

This repository studies an explicit map \(F:\mathbb C^3\to\mathbb C^3\) for which:

1. the Jacobian determinant is the constant \(-2\), but
2. three distinct points have the same image.

If both exact identities are correct—and the included checks are designed to make them independently reproducible—then the Jacobian Conjecture is false in dimension 3 and therefore in every dimension \(n\ge 3\).

---

## The decisive certificate

Set

\[
s=xy,\qquad u=1+s,
\]

and define

\[
\begin{aligned}
F_1(x,y,z)&=u^3z+y^2u(4+3s),\\
F_2(x,y,z)&=y+3xu^2z+3xy^2(4+3s),\\
F_3(x,y,z)&=2x-3x^2y-x^3z.
\end{aligned}
\]

The central claim reduces to these two exact calculations:

### 1. Constant nonzero Jacobian

\[
\det J_F\equiv -2.
\]

This makes \(F\) a **Keller map**: it is locally invertible everywhere.

### 2. Explicit failure of injectivity

The three distinct points

\[
(0,0,-1/4),\qquad (1,-3/2,13/2),\qquad (-1,3/2,13/2)
\]

all map to

\[
(-1/4,0,0).
\]

No numerical approximation is involved. Both claims are polynomial identities over the rationals.

---

## Verify it yourself

### Fastest verification

```bash
python -m pip install -r requirements.txt
python checks/check_1_determinant.py
python checks/check_2_collision.py
```

These are the only two checks needed for the central counterexample claim.

Expected result:

```text
PASS check_1_determinant
PASS check_2_collision
```

### Run the complete six-check certificate

```bash
make verify
```

or

```bash
python scripts/run_all_checks.py
```

The full certificate independently checks:

| Check | What it verifies |
|---|---|
| 1 | \(\det J_F=-2\) exactly |
| 2 | Three distinct rational points have one image |
| 3 | The generic fiber degree is 3 |
| 4 | The exact Jelonek non-properness surface |
| 5 | The constructible fiber pattern \(3/1/0\) |
| 6 | Full \(S_3\) Galois structure and transposition monodromy |

Every certified check is standalone, assert-based, and uses exact SymPy arithmetic. No floating point is used in any certified conclusion.

### Verify package integrity

```bash
make integrity
```

This verifies both the original frozen referee package and the GitHub repository manifest.

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for environments, commands, expected output, and independent reimplementation guidance.

---

## What is the “Fable Pattern”?

The determinant-and-collision certificate establishes the claimed counterexample. The later calculations explain **how** a map can be locally invertible everywhere and still fail globally.

The map behaves generically like a three-sheeted cover:

\[
\boxed{3\longrightarrow 1\longrightarrow 0}
\]

- **Away from the Jelonek surface:** a generic target has 3 preimages.
- **On most of the Jelonek surface:** 2 sheets escape to infinity and 1 finite sheet survives.
- **On a special curve \(\Gamma\) inside that surface:** the surviving sheet also escapes, leaving no finite preimage.

The sheets do not collide at a critical point—the Jacobian never vanishes. Instead, global invertibility fails through structured escape at infinity.

This recurring mechanism is what the project informally calls the **Fable Pattern**:

> A locally étale polynomial map can fail globally when sheets of a finite cover escape over a structured non-properness hypersurface, with monodromy controlling which sheets leave and which survive.

For the present map, the escaping pair is exchanged by a transposition, the generic covering group is \(S_3\), and the exact fiber stratification is:

| Target stratum | Number of finite preimages |
|---|---:|
| \(\mathbb C^3\setminus S_F\) | 3 |
| \(S_F\setminus\Gamma\) | 1 |
| \(\Gamma\) | 0 |

These structural results are not needed to establish the central claim; they explain its geometry.

---

## Where should I start?

### I want the shortest possible review

1. Read the map and central claim in this README.
2. Run Checks 1 and 2.
3. Inspect [PAPER_I.md](PAPER_I.md), which states the frozen submission claim and check matrix.

### I am an algebraic geometer

1. Read [PAPER_I.md](PAPER_I.md).
2. Reimplement Checks 1 and 2 in your preferred CAS.
3. Audit Checks 3–6 independently.
4. Review [docs/STRATA.md](docs/STRATA.md) for the \(3/1/0\) fiber theorem.
5. Review [docs/JELONEK_GALOIS.md](docs/JELONEK_GALOIS.md) together with its noted supersessions.

### I am a computer-algebra reviewer

Start in [`checks/`](checks/). Each file defines the map from scratch and imports only SymPy. The scripts are intentionally independent so that a failure in one does not contaminate the others.

### I want the broader theory

Read [PAPER_II_INDEX.md](PAPER_II_INDEX.md). Paper II contains the structural consequences developed after the map was found, including:

- degree minimality;
- the Jelonek–monodromy–divisor formulation of the Galois obstruction;
- Orevkov’s cubic-plane theorem in ledger language;
- the constructible defect ledger;
- the cubic silent-cycle identity;
- explicitly labeled open problems.

**Paper II is held separately from the central submission.** Its claims are not required for Paper I.

---

## Repository map

```text
PAPER_I.md                 Frozen submission document and claim matrix
PAPER_II_INDEX.md          Index of held structural work and rigor labels
checks/                    Six independent certification scripts
scripts/                   Full research and derivation scripts
docs/                      Detailed mathematical development
frozen/                    Original frozen referee archive and checksum
legacy/                    Session provenance; not needed for verification
REPRODUCIBILITY.md         Exact reproduction protocol
REPOSITORY_GUIDE.md        Review order and integrity boundaries
CONTRIBUTING.md            How to report reproductions or mathematical issues
MANIFEST.sha256            Manifest of the original frozen referee package
REPOSITORY_MANIFEST.sha256 Manifest of the GitHub-ready repository
```

---

## Claim boundaries

| Layer | Status | Required for central claim? |
|---|---|---:|
| Constant Jacobian identity | Exact, frozen, independently executable | Yes |
| Explicit three-point collision | Exact, frozen, independently executable | Yes |
| Generic degree, Jelonek surface, \(3/1/0\) strata, \(S_3\) structure | Exact package computations | No |
| Paper II structural consequences | Held for separate review; rigor-labeled | No |
| Universal silent-divisor and adjunction programs | Open research | No |

The repository deliberately separates a small finite certificate from the larger explanatory theory. A flaw in a Paper II interpretation does not alter the determinant-and-collision calculation.

---

## How to report a result

Please use the GitHub issue templates:

- **Independent verification report** for a successful or failed reproduction.
- **Mathematical issue** for a precise objection, failed assertion, or missing implication.

A useful report includes:

- the exact file or numbered claim;
- operating system and CAS versions;
- the commands run;
- complete unedited output;
- a minimal countercalculation when reporting an error.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the review policy.

---

## Provenance and attribution

The map is attributed to **L. Alpöge**, produced in interaction with an AI system referred to as **Fable**, and posted publicly on July 19, 2026. This repository claims no priority over the map itself. Its purpose is to preserve and expose an independently checkable certificate and the subsequent geometric analysis.

See [NOTICE.md](NOTICE.md), [CITATION.cff](CITATION.cff), and [LICENSE_NOTICE.md](LICENSE_NOTICE.md) before reusing or redistributing material.

---

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). Until external review is complete, please describe the result as a **claimed, independently checkable counterexample** rather than as an established resolution of the Jacobian Conjecture.
