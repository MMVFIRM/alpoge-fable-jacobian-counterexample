# Reproducibility

## Reference environment

- Python 3.11
- SymPy 1.14.0
- Linux

The GitHub workflow also runs the frozen checks on Python 3.12 and 3.13.

## One-command verification

```bash
python -m pip install -r requirements.txt
python scripts/run_all_checks.py
```

or:

```bash
make install
make verify
```

## Minimal central verification

```bash
python checks/check_1_determinant.py
python checks/check_2_collision.py
```

The first expands the Jacobian determinant exactly. The second evaluates the map at three distinct rational points exactly. Neither uses floating point.

## Independent reimplementation

Reviewers are encouraged to reproduce the two central checks in another computer algebra system such as Magma, Maple, Mathematica, SageMath, Singular, or Macaulay2. The complete map formulas and target points appear in `PAPER_I.md`.

## Integrity

```bash
make frozen-files-integrity
make frozen-archive-integrity
make repository-integrity
```

`MANIFEST.sha256` belongs to the original frozen package. `REPOSITORY_MANIFEST.sha256` covers the expanded GitHub repository.
