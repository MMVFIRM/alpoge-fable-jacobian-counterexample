# Repository guide

This repository preserves the frozen referee package and adds only GitHub-oriented infrastructure around it.

## Review order

1. Read `PAPER_I.md`.
2. Run `checks/check_1_determinant.py` and `checks/check_2_collision.py`.
3. Run `python scripts/run_all_checks.py` for the complete six-check certificate.
4. Inspect `PAPER_II_INDEX.md` only after Paper I has received independent review.

## Integrity boundaries

- The files listed by `MANIFEST.sha256` are the original frozen referee package.
- `frozen/referee_package-2026-07-20.zip` is the exact source archive used to construct this repository.
- GitHub CI, issue templates, and repository guidance are additive and are not mathematical evidence.
- `REPOSITORY_MANIFEST.sha256` covers the complete GitHub-ready tree except itself and ordinary Git metadata.

## Repository policy

Paper I is the independently checkable central claim. Paper II contains structural consequences, literature-sensitive interpretations, and open research. Pull requests must keep that boundary explicit.
