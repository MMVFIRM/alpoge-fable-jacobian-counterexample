"""
conjecture_tester.py  —  GeoVerify, extended into a conjecture-testing harness
==============================================================================
GeoVerify (core.py) answers "are these two EXPRESSIONS equal?"  That is the
*verify* half of a generate-and-verify loop, but restricted to expression
equivalence and — as the benchmark exposed — brittle on the LaTeX string path
(dropped subscripts, function-call ambiguity, real-only numeric sampling).

This module turns that verify-core into something I can actually drive against
conjectures. It works on SymPy objects (not fragile LaTeX strings) and adds:

  1. prove_or_refute_identity  — symbolic first, then COMPLEX numeric sampling
                                 (fixes GeoVerify's real-positive-only blind spot)
  2. check_candidate           — does an object satisfy a hypothesis but break
                                 the conclusion?  (the Jacobian pattern, general)
  3. search_counterexample     — iterate a candidate space, return first witness
  4. domain checkers           — polynomial-map (Jacobian family) + Diophantine

Every returned verdict carries HOW it was reached and a concrete witness, so a
"counterexample" is always an object you can independently re-check.
"""
import itertools
import sympy as sp
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Any, List, Tuple


@dataclass
class Verdict:
    status: str              # "identity" | "refuted" | "consistent" | "counterexample" | "none_found"
    method: str
    witness: Any = None      # concrete object proving the verdict
    detail: dict = field(default_factory=dict)

    def __repr__(self):
        w = f", witness={self.witness}" if self.witness is not None else ""
        return f"Verdict({self.status} via {self.method}{w})"


class ConjectureTester:
    def __init__(self, numeric_samples: int = 40, seed: int = 12345):
        self.numeric_samples = numeric_samples
        self._rng = sp.ntheory.residue_ntheory  # placeholder; we use python rng below
        import random
        self._random = random.Random(seed)

    # ----------------------------------------------------------------- #
    # 1. Identity checking: symbolic, then complex-plane numeric         #
    # ----------------------------------------------------------------- #
    def prove_or_refute_identity(self, lhs, rhs, syms=None) -> Verdict:
        """
        Decide whether lhs == rhs as functions.
        - If simplify(lhs-rhs)==0  -> proven identity.
        - Else sample at random COMPLEX points. A single mismatch REFUTES
          (with the witness point). All-match -> 'consistent' (strong evidence,
          not a proof).
        """
        lhs, rhs = sp.sympify(lhs), sp.sympify(rhs)
        diff = lhs - rhs
        if syms is None:
            syms = sorted(diff.free_symbols, key=str)

        # symbolic attempt
        try:
            s = sp.simplify(diff)
            if s == 0:
                return Verdict("identity", "symbolic_simplify_zero")
        except Exception:
            pass
        try:
            s2 = sp.expand(sp.cancel(diff))
            if s2 == 0:
                return Verdict("identity", "expand_cancel_zero")
        except Exception:
            pass

        # complex numeric sampling (the fix for GeoVerify's real-only blind spot)
        f = sp.lambdify(syms, diff, modules="mpmath") if syms else None
        mismatches = 0
        for _ in range(self.numeric_samples):
            pt = [sp.Float(self._random.uniform(-3, 3)) + sp.I*sp.Float(self._random.uniform(-3, 3))
                  for _ in syms]
            try:
                val = complex(diff.subs(dict(zip(syms, pt))).evalf()) if syms else complex(diff.evalf())
            except Exception:
                continue
            if abs(val) > 1e-9:
                return Verdict("refuted", "complex_numeric_mismatch",
                               witness={str(s): complex(p) for s, p in zip(syms, pt)},
                               detail={"|lhs-rhs|": abs(val)})
        return Verdict("consistent", "complex_numeric_allmatch",
                       detail={"samples": self.numeric_samples})

    # ----------------------------------------------------------------- #
    # 2. Candidate check: satisfies hypothesis, violates conclusion?     #
    # ----------------------------------------------------------------- #
    def check_candidate(self, candidate, hypothesis: Callable[[Any], bool],
                        conclusion: Callable[[Any], bool]) -> Verdict:
        """A candidate is a counterexample iff hypothesis(c) and not conclusion(c)."""
        try:
            if not hypothesis(candidate):
                return Verdict("none_found", "hypothesis_fails", detail={"candidate": candidate})
            if conclusion(candidate):
                return Verdict("none_found", "conclusion_holds", detail={"candidate": candidate})
            return Verdict("counterexample", "hypothesis_true_conclusion_false", witness=candidate)
        except Exception as e:
            return Verdict("none_found", f"error:{type(e).__name__}", detail={"msg": str(e)})

    # ----------------------------------------------------------------- #
    # 3. Search a candidate space                                         #
    # ----------------------------------------------------------------- #
    def search_counterexample(self, space: Iterable, is_counterexample: Callable[[Any], bool],
                              max_checks: Optional[int] = None) -> Verdict:
        checked = 0
        for cand in space:
            if max_checks is not None and checked >= max_checks:
                break
            checked += 1
            try:
                if is_counterexample(cand):
                    return Verdict("counterexample", "search_hit", witness=cand,
                                   detail={"checked": checked})
            except Exception:
                continue
        return Verdict("none_found", "search_exhausted", detail={"checked": checked})

    # ----------------------------------------------------------------- #
    # 4a. Domain checker: polynomial self-maps (Jacobian family)         #
    # ----------------------------------------------------------------- #
    def jacobian_det(self, F: List, vars: List):
        J = sp.Matrix(F).jacobian(sp.Matrix(vars))
        return sp.expand(J.det())

    def is_constant_nonzero_jacobian(self, F, vars) -> Tuple[bool, Any]:
        d = self.jacobian_det(F, vars)
        return (d.free_symbols == set() and d != 0), d

    def collide(self, F, vars, points) -> Optional[Tuple]:
        """Return a pair of distinct points with equal image, else None (proves non-injectivity)."""
        seen = {}
        for p in points:
            img = tuple(sp.simplify(comp.subs(dict(zip(vars, p)))) for comp in F)
            if img in seen and seen[img] != tuple(p):
                return (seen[img], tuple(p), img)
            seen[img] = tuple(p)
        return None

    def test_jacobian_counterexample(self, F, vars, witness_points) -> Verdict:
        """Full Jacobian-Conjecture-style check: constant nonzero Jacobian AND non-injective."""
        const, d = self.is_constant_nonzero_jacobian(F, vars)
        if not const:
            return Verdict("none_found", "jacobian_not_constant_nonzero", detail={"det": d})
        coll = self.collide(F, vars, witness_points)
        if coll is None:
            return Verdict("consistent", "no_collision_found_in_points", detail={"det": d})
        return Verdict("counterexample", "constant_jacobian_but_noninjective",
                       witness={"p1": coll[0], "p2": coll[1], "image": coll[2]},
                       detail={"jacobian_det": d})

    # ----------------------------------------------------------------- #
    # 4b. Domain checker: Diophantine equality of integer power sums     #
    # ----------------------------------------------------------------- #
    def is_perfect_power(self, N: int, k: int) -> Optional[int]:
        """Return m with m**k == N (m>0) if it exists, else None."""
        if N <= 0:
            return None
        lo, hi = 1, int(round(N ** (1.0 / k))) + 2
        for m in range(max(1, lo), hi + 1):
            p = m ** k
            if p == N:
                return m
            if p > N:
                break
        return None
