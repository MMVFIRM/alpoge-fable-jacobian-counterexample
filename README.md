# Referee package — Alpöge–Fable counterexample to the Jacobian Conjecture

FROZEN PACKAGE. No further research content; production consolidation only.

## Quick start (10 seconds to the central claim)

    pip install sympy
    python3 checks/check_1_determinant.py   # det J_F = -2      (Keller)
    python3 checks/check_2_collision.py     # 3 points, 1 image (non-injective)

These two checks alone falsify the Jacobian Conjecture in dimension 3.

## Layout

    PAPER_I.md            the submission document: map, claims, check matrix
    PAPER_II_INDEX.md     structural-consequences documents (HELD, not submitted)
    checks/               six independent, standalone, assert-based scripts
        check_1_determinant.py     det J = -2
        check_2_collision.py       three distinct points, one image
        check_3_degree.py          generic degree 3 (master identity, Groebner)
        check_4_jelonek_surface.py the exact non-properness surface
        check_5_stratification.py  fibers 3/1/0; F misses exactly Gamma
        check_6_galois.py          S3, transposition meridian (exact parity)
    docs/                 all session Markdown documents (Papers I+II material)
    scripts/              the full research scripts (superset of checks/)
    legacy/               GeoVerify equivalence-checker + conjecture-tester
                          (session provenance; not needed for verification)
    MANIFEST.sha256       SHA-256 of every file in this package

## Verification protocol

Each check is independent: it imports only sympy, defines the map from
scratch, and asserts its claims (nonzero exit on failure). Reviewers may
divide the checks among themselves; the union of PASSes certifies every
claim in PAPER_I.md. All computations are exact (rational/symbolic); no
floating point enters any certified claim.

Environment used to freeze this package: Python 3.11, SymPy 1.14.0, Linux.
Total sequential runtime of all six checks: under 10 minutes on one CPU.

## Status of Paper II

docs/ contains the structural-consequence documents through part 8, with the
final audit's three repairs applied (residue-degree wording; H²-conductor
claim downgraded to open; adjunction reclassified as future research). They
are indexed with rigor labels in PAPER_II_INDEX.md and are to be held until
Paper I survives outside verification.
