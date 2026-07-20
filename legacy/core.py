"""
GeoVerify: Geometric Equivalence Checking for Mathematical Objects
"""
import re
import hashlib
import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class TimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

def with_timeout(func, timeout_sec=5, default=None):
    import signal as _signal
    try:
        old_handler = _signal.signal(_signal.SIGALRM, _timeout_handler)
        _signal.alarm(timeout_sec)
        try:
            result = func()
        finally:
            _signal.alarm(0)
            _signal.signal(_signal.SIGALRM, old_handler)
        return result
    except TimeoutError:
        return default
    except Exception:
        return default

import sympy
from sympy import (
    sympify, simplify, expand, factor, cancel, trigsimp,
    symbols, Symbol, Function, Eq, oo, pi, I, E,
    sin, cos, tan, exp, log, sqrt, Abs, Rational,
    Matrix, Piecewise, Interval, FiniteSet, Union,
    latex as sympy_latex
)
from sympy.core.relational import Relational
from sympy.parsing.latex import parse_latex

class EquivalenceResult(Enum):
    EQUIVALENT = "equivalent"
    NOT_EQUIVALENT = "not_equivalent"
    UNCERTAIN = "uncertain"

@dataclass
class VerificationResult:
    decision: EquivalenceResult
    confidence: float
    method: str
    details: Dict[str, Any]

class LaTeXNormalizer:
    @staticmethod
    def normalize(latex_str: str) -> str:
        s = latex_str.strip()
        s = LaTeXNormalizer._strip_text_wrappers(s)
        s = LaTeXNormalizer._normalize_commands(s)
        s = LaTeXNormalizer._normalize_whitespace(s)
        s = LaTeXNormalizer._normalize_notation(s)
        return s

    @staticmethod
    def _strip_text_wrappers(s: str) -> str:
        patterns = [
            r'^The\s+(generating\s+function|answer|result|solution|expression)\s+(is|equals?)\s*',
            r'^(?:Therefore|Thus|Hence|So),?\s*',
            r'^\s*(?:for|where|when)\s+.*?[,;:]\s*',
        ]
        for pat in patterns:
            s = re.sub(pat, '', s, flags=re.IGNORECASE)
        s = s.strip().rstrip('.')
        return s

    @staticmethod
    def _normalize_commands(s: str) -> str:
        s = re.sub(r'\\mathrm\{i\}', 'i', s)
        s = re.sub(r'\\mathrm\{e\}', 'e', s)
        s = re.sub(r'\\mathrm\{d\}', 'd', s)
        s = re.sub(r'\\text\{(\s*(?:if|for|when|otherwise|and|or|where)\s*)\}', r' \1 ', s)
        s = re.sub(r'\\text\{([^}]*)\}', r'\1', s)
        s = re.sub(r'\\textrm\{([^}]*)\}', r'\1', s)
        s = re.sub(r'\\textit\{([^}]*)\}', r'\1', s)
        s = re.sub(r'\\left\s*', '', s)
        s = re.sub(r'\\right\s*', '', s)
        s = re.sub(r'\\(?:display|script|scriptscript|text)style\s*', '', s)
        s = re.sub(r'\\dfrac', r'\\frac', s)
        s = re.sub(r'\\tfrac', r'\\frac', s)
        s = re.sub(r'\s*\\cdot\s*', ' ', s)
        s = re.sub(r'\s*\\times\s*', ' ', s)
        s = re.sub(r'\\geq\b', r'\\ge', s)
        s = re.sub(r'\\leq\b', r'\\le', s)
        s = re.sub(r'\\(?:mathbf|boldsymbol|mathbb|mathcal|mathfrak)\{([^}]*)\}', r'\1', s)
        s = re.sub(r'\\[,;:!]', ' ', s)
        s = re.sub(r'\\q?quad\s*', ' ', s)
        return s

    @staticmethod
    def _normalize_whitespace(s: str) -> str:
        s = re.sub(r'\s+', ' ', s)
        return s.strip()

    @staticmethod
    def _normalize_notation(s: str) -> str:
        s = re.sub(r'\\lvert\s*', '|', s)
        s = re.sub(r'\\rvert\s*', '|', s)
        s = re.sub(r'\\\|', '|', s)
        return s

class SymbolicParser:
    @staticmethod
    def parse(latex_str: str) -> Optional[sympy.Basic]:
        result = SymbolicParser._try_sympy_latex_parser(latex_str)
        if result is not None:
            return result
        result = SymbolicParser._try_latex2sympy(latex_str)
        if result is not None:
            return result
        result = SymbolicParser._try_manual_parse(latex_str)
        if result is not None:
            return result
        return None

    @staticmethod
    def _try_sympy_latex_parser(latex_str: str) -> Optional[sympy.Basic]:
        try:
            return parse_latex(latex_str)
        except Exception:
            return None

    @staticmethod
    def _try_latex2sympy(latex_str: str) -> Optional[sympy.Basic]:
        try:
            from latex2sympy2 import latex2sympy
            return latex2sympy(latex_str)
        except Exception:
            return None

    @staticmethod
    def _try_manual_parse(latex_str: str) -> Optional[sympy.Basic]:
        try:
            s = latex_str
            s = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', s)
            s = re.sub(r'\\sqrt\{([^}]*)\}', r'sqrt(\1)', s)
            s = re.sub(r'\\pi', 'pi', s)
            s = re.sub(r'\\infty', 'oo', s)
            s = re.sub(r'\\sin', 'sin', s)
            s = re.sub(r'\\cos', 'cos', s)
            s = re.sub(r'\\tan', 'tan', s)
            s = re.sub(r'\\exp', 'exp', s)
            s = re.sub(r'\\ln', 'log', s)
            s = re.sub(r'\\log', 'log', s)
            s = re.sub(r'\^{([^}]*)}', r'**(\1)', s)
            s = re.sub(r'\^(.)', r'**\1', s)
            s = re.sub(r'_\{[^}]*\}', '', s)
            s = re.sub(r'\\[a-zA-Z]+', '', s)
            s = re.sub(r'[{}]', '', s)
            s = s.strip()
            if s:
                return sympify(s)
        except Exception:
            pass
        return None

class AlgebraicCanonicalizer:
    @staticmethod
    def canonicalize(expr: sympy.Basic) -> sympy.Basic:
        if expr is None:
            return None
        try:
            canon = with_timeout(lambda: sympy.expand(expr), timeout_sec=2, default=expr)
            canon = with_timeout(lambda: sympy.cancel(canon), timeout_sec=2, default=canon)
            canon = with_timeout(lambda: sympy.trigsimp(canon), timeout_sec=2, default=canon)
            canon = with_timeout(lambda: sympy.simplify(canon), timeout_sec=2, default=canon)
            return canon
        except Exception:
            return expr

class GeometricSignature:
    @dataclass
    class Signature:
        tree_depth: int
        num_operations: int
        operation_spectrum: Dict[str, int]
        constants: List[float]
        num_free_symbols: int
        structural_hash: str
        degree_info: Optional[Dict[str, int]]
        complexity: int

        def distance(self, other: 'GeometricSignature.Signature') -> float:
            if self.structural_hash == other.structural_hash:
                return 0.0
            d = 0.0
            d += abs(self.tree_depth - other.tree_depth) * 0.5
            d += abs(self.num_operations - other.num_operations) * 0.3
            d += abs(self.num_free_symbols - other.num_free_symbols) * 2.0
            all_ops = set(self.operation_spectrum.keys()) | set(other.operation_spectrum.keys())
            for op in all_ops:
                d += abs(self.operation_spectrum.get(op, 0) -
                        other.operation_spectrum.get(op, 0)) * 0.2
            c1 = self.constants
            c2 = other.constants
            if len(c1) != len(c2):
                d += abs(len(c1) - len(c2)) * 1.0
            else:
                for a, b in zip(c1, c2):
                    if a != b:
                        d += 0.5
            d += abs(self.complexity - other.complexity) * 0.1
            return d

    @staticmethod
    def extract(expr: sympy.Basic) -> Optional['GeometricSignature.Signature']:
        if expr is None:
            return None
        try:
            depth = GeometricSignature._tree_depth(expr)
            op_spec = GeometricSignature._operation_spectrum(expr)
            num_ops = sum(op_spec.values())
            constants = sorted([float(n) for n in expr.atoms(sympy.Number)
                              if n not in (sympy.S.Zero, sympy.S.One, sympy.S.NegativeOne)])
            num_free = len(expr.free_symbols)
            struct_hash = GeometricSignature._structural_hash(expr)
            degree_info = GeometricSignature._degree_info(expr)
            try:
                complexity = sympy.count_ops(expr)
            except Exception:
                complexity = 0
            return GeometricSignature.Signature(
                tree_depth=depth,
                num_operations=num_ops,
                operation_spectrum=op_spec,
                constants=constants,
                num_free_symbols=num_free,
                structural_hash=struct_hash,
                degree_info=degree_info,
                complexity=complexity
            )
        except Exception:
            return None

    @staticmethod
    def _tree_depth(expr: sympy.Basic) -> int:
        if not expr.args:
            return 0
        return 1 + max(GeometricSignature._tree_depth(a) for a in expr.args)

    @staticmethod
    def _operation_spectrum(expr: sympy.Basic) -> Dict[str, int]:
        spec = {}
        def walk(e):
            if e.args:
                name = type(e).__name__
                spec[name] = spec.get(name, 0) + 1
                for a in e.args:
                    walk(a)
        walk(expr)
        return spec

    @staticmethod
    def _structural_hash(expr: sympy.Basic) -> str:
        try:
            free = sorted(expr.free_symbols, key=lambda s: str(s))
            canonical_syms = [Symbol(f'x_{i}') for i in range(len(free))]
            sub_dict = dict(zip(free, canonical_syms))
            canonical_expr = expr.subs(sub_dict)
            canon_str = str(canonical_expr)
            return hashlib.md5(canon_str.encode()).hexdigest()
        except Exception:
            return hashlib.md5(str(expr).encode()).hexdigest()

    @staticmethod
    def _degree_info(expr: sympy.Basic) -> Optional[Dict[str, int]]:
        try:
            free = expr.free_symbols
            if not free:
                return {}
            result = {}
            for s in free:
                try:
                    p = sympy.Poly(expr, s)
                    result[str(s)] = p.degree()
                except Exception:
                    pass
            return result if result else None
        except Exception:
            return None

class GeoVerifier:
    def __init__(self, verbose: bool = False):
        self.normalizer = LaTeXNormalizer()
        self.parser = SymbolicParser()
        self.canonicalizer = AlgebraicCanonicalizer()
        self.verbose = verbose

    def verify(self, reference: str, prediction: str,
               problem_statement: str = "", _depth: int = 0) -> VerificationResult:
        details = {}
        norm_ref = self.normalizer.normalize(reference)
        norm_pred = self.normalizer.normalize(prediction)
        details['normalized_ref'] = norm_ref
        details['normalized_pred'] = norm_pred
        if norm_ref == norm_pred:
            return VerificationResult(
                decision=EquivalenceResult.EQUIVALENT,
                confidence=1.0,
                method="exact_string_match",
                details=details
            )
        try:
            from structural import LaTeXStructuralAnalyzer
            sa = LaTeXStructuralAnalyzer()
            struct_equiv, struct_conf, struct_method = sa.structural_equivalent(norm_ref, norm_pred)
            details['structural_method'] = struct_method
            details['structural_confidence'] = struct_conf
            if struct_equiv and struct_conf >= 0.85:
                return VerificationResult(
                    decision=EquivalenceResult.EQUIVALENT,
                    confidence=struct_conf,
                    method=f"structural:{struct_method}",
                    details=details
                )
            elif not struct_equiv and struct_conf >= 0.70:
                details['structural_non_equiv'] = True
                details['structural_non_equiv_conf'] = struct_conf
        except Exception as e:
            details['structural_error'] = str(e)
        ref_expr = self.parser.parse(norm_ref)
        pred_expr = self.parser.parse(norm_pred)
        details['ref_parsed'] = ref_expr is not None
        details['pred_parsed'] = pred_expr is not None
        if ref_expr is not None and pred_expr is not None:
            try:
                diff = with_timeout(
                    lambda: sympy.simplify(ref_expr - pred_expr),
                    timeout_sec=3, default=None)
                if diff is not None and diff == 0:
                    return VerificationResult(
                        decision=EquivalenceResult.EQUIVALENT,
                        confidence=0.98,
                        method="symbolic_simplify_zero",
                        details=details
                    )
            except Exception:
                pass
            canon_ref = with_timeout(
                lambda: self.canonicalizer.canonicalize(ref_expr),
                timeout_sec=3, default=ref_expr)
            canon_pred = with_timeout(
                lambda: self.canonicalizer.canonicalize(pred_expr),
                timeout_sec=3, default=pred_expr)
            if canon_ref is not None and canon_pred is not None:
                try:
                    diff = with_timeout(
                        lambda: sympy.simplify(canon_ref - canon_pred),
                        timeout_sec=3, default=None)
                    if diff is not None and diff == 0:
                        return VerificationResult(
                            decision=EquivalenceResult.EQUIVALENT,
                            confidence=0.97,
                            method="canonical_simplify_zero",
                            details=details
                        )
                except Exception:
                    pass
                try:
                    if canon_pred != 0:
                        ratio = with_timeout(
                            lambda: sympy.simplify(canon_ref / canon_pred),
                            timeout_sec=3, default=None)
                        if ratio is not None and ratio == 1:
                            return VerificationResult(
                                decision=EquivalenceResult.EQUIVALENT,
                                confidence=0.96,
                                method="ratio_test",
                                details=details
                            )
                except Exception:
                    pass
                result = self._numerical_equivalence_test(
                    canon_ref, canon_pred, details)
                if result is not None:
                    return result
            sig_ref = GeometricSignature.extract(
                canon_ref if canon_ref is not None else ref_expr)
            sig_pred = GeometricSignature.extract(
                canon_pred if canon_pred is not None else pred_expr)
            if sig_ref is not None and sig_pred is not None:
                distance = sig_ref.distance(sig_pred)
                details['signature_distance'] = distance
                details['sig_ref_hash'] = sig_ref.structural_hash
                details['sig_pred_hash'] = sig_pred.structural_hash
                if sig_ref.structural_hash == sig_pred.structural_hash:
                    return VerificationResult(
                        decision=EquivalenceResult.EQUIVALENT,
                        confidence=0.95,
                        method="structural_hash_match",
                        details=details
                    )
                if distance == 0.0:
                    return VerificationResult(
                        decision=EquivalenceResult.EQUIVALENT,
                        confidence=0.90,
                        method="zero_signature_distance",
                        details=details
                    )
                if distance > 5.0:
                    return VerificationResult(
                        decision=EquivalenceResult.NOT_EQUIVALENT,
                        confidence=min(0.95, 0.5 + distance * 0.05),
                        method="high_signature_distance",
                        details=details
                    )
        result = self._fuzzy_string_comparison(norm_ref, norm_pred, details)
        if result is not None:
            return result
        if _depth < 2:
            result = self._equation_aware_comparison(norm_ref, norm_pred, details, _depth)
            if result is not None:
                return result
        result = self._prefix_difference_detection(norm_ref, norm_pred, details)
        if result is not None:
            return result
        if details.get('structural_non_equiv', False):
            return VerificationResult(
                decision=EquivalenceResult.NOT_EQUIVALENT,
                confidence=details.get('structural_non_equiv_conf', 0.5),
                method="structural_non_equiv_fallback",
                details=details
            )
        return VerificationResult(
            decision=EquivalenceResult.UNCERTAIN,
            confidence=0.3,
            method="no_conclusive_method",
            details=details
        )

    def _equation_aware_comparison(self, s1, s2, details, _depth=0):
        if '=' not in s1 or '=' not in s2:
            return None
        if re.search(r'\\[lg]eq|\\neq|\\approx|<=|>=|!=', s1):
            return None
        try:
            lhs1, rhs1 = self._split_equation(s1)
            lhs2, rhs2 = self._split_equation(s2)
            if lhs1 is None or lhs2 is None:
                return None
            lhs_match = (lhs1.strip() == lhs2.strip())
            if lhs_match:
                rhs_result = self.verify(rhs1.strip(), rhs2.strip(), _depth=_depth+1)
                if rhs_result.decision == EquivalenceResult.EQUIVALENT:
                    return VerificationResult(
                        decision=EquivalenceResult.EQUIVALENT,
                        confidence=rhs_result.confidence * 0.95,
                        method=f"equation_rhs:{rhs_result.method}",
                        details=details
                    )
                elif rhs_result.decision == EquivalenceResult.NOT_EQUIVALENT:
                    return VerificationResult(
                        decision=EquivalenceResult.NOT_EQUIVALENT,
                        confidence=rhs_result.confidence * 0.95,
                        method=f"equation_rhs_diff:{rhs_result.method}",
                        details=details
                    )
        except Exception:
            pass
        return None

    def _split_equation(self, s):
        depth = 0
        for i, c in enumerate(s):
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            elif c == '=' and depth == 0:
                before = s[max(0,i-4):i]
                if '\\' not in before or before.endswith(' '):
                    return s[:i], s[i+1:]
        return None, None

    def _prefix_difference_detection(self, s1, s2, details):
        c1 = re.sub(r'\s+', '', s1)
        c2 = re.sub(r'\s+', '', s2)
        if len(c1) > len(c2) and c1.endswith(c2):
            prefix = c1[:len(c1)-len(c2)]
            if prefix in ('2', '3', '-', '-1', '2*', '3*', '-1*'):
                return VerificationResult(
                    decision=EquivalenceResult.NOT_EQUIVALENT,
                    confidence=0.88, method=f"prefix_diff:{prefix}", details=details)
        if len(c2) > len(c1) and c2.endswith(c1):
            prefix = c2[:len(c2)-len(c1)]
            if prefix in ('2', '3', '-', '-1', '2*', '3*', '-1*'):
                return VerificationResult(
                    decision=EquivalenceResult.NOT_EQUIVALENT,
                    confidence=0.88, method=f"prefix_diff:{prefix}", details=details)
        if c2 == '-' + c1 or c1 == '-' + c2:
            return VerificationResult(
                decision=EquivalenceResult.NOT_EQUIVALENT,
                confidence=0.92, method="negation_prefix", details=details)
        if len(c1) == len(c2):
            diffs = [(i, c1[i], c2[i]) for i in range(len(c1)) if c1[i] != c2[i]]
            if 1 <= len(diffs) <= 2:
                all_numeric_diff = all(a.isdigit() or b.isdigit() for _, a, b in diffs)
                if all_numeric_diff:
                    return VerificationResult(
                        decision=EquivalenceResult.NOT_EQUIVALENT,
                        confidence=0.85, method=f"char_diff:{diffs}", details=details)
                if len(diffs) >= 1:
                    return VerificationResult(
                        decision=EquivalenceResult.NOT_EQUIVALENT,
                        confidence=0.78, method=f"char_diff_func:{len(diffs)}_diffs", details=details)
        len_diff = abs(len(c1) - len(c2))
        if len_diff == 0 and len(c1) > 5:
            diffs_with_context = []
            for i in range(len(c1)):
                if c1[i] != c2[i]:
                    ctx_before = c1[max(0,i-3):i]
                    diffs_with_context.append((i, c1[i], c2[i], ctx_before))
            if 1 <= len(diffs_with_context) <= 2:
                has_subscript_context = any('_' in ctx for _, _, _, ctx in diffs_with_context)
                has_numeric_change = any(a.isdigit() and b.isdigit() for _, a, b, _ in diffs_with_context)
                if has_subscript_context and has_numeric_change:
                    return VerificationResult(
                        decision=EquivalenceResult.NOT_EQUIVALENT,
                        confidence=0.88, method=f"subscript_digit_change:{diffs_with_context}", details=details)
        if 0 < len_diff <= 3 and min(len(c1), len(c2)) > 10:
            shorter = c1 if len(c1) < len(c2) else c2
            longer = c1 if len(c1) >= len(c2) else c2
            prefix_match = 0
            for i in range(min(len(shorter), len(longer))):
                if shorter[i] == longer[i]:
                    prefix_match += 1
                else:
                    break
            suffix_match = 0
            for i in range(1, min(len(shorter), len(longer)) + 1):
                if shorter[-i] == longer[-i]:
                    suffix_match += 1
                else:
                    break
            coverage = (prefix_match + suffix_match) / len(shorter)
            if coverage > 0.90:
                return VerificationResult(
                    decision=EquivalenceResult.NOT_EQUIVALENT,
                    confidence=0.80, method=f"near_match_diff:{len_diff}chars", details=details)

    def _numerical_equivalence_test(self, expr1, expr2, details):
        try:
            free1 = expr1.free_symbols
            free2 = expr2.free_symbols
            if len(free1) != len(free2):
                return None
            syms1 = sorted(free1, key=str)
            syms2 = sorted(free2, key=str)
            np.random.seed(42)
            n_tests = 10
            n_pass = 0
            for _ in range(n_tests):
                vals = {s: np.random.uniform(0.1, 5.0) for s in syms1}
                vals2 = {s2: vals[s1] for s1, s2 in zip(syms1, syms2)}
                try:
                    v1 = complex(expr1.subs(vals))
                    v2 = complex(expr2.subs(vals2))
                    if abs(v1) < 1e-15 and abs(v2) < 1e-15:
                        n_pass += 1
                    elif abs(v1) > 1e-15:
                        rel_diff = abs(v1 - v2) / abs(v1)
                        if rel_diff < 1e-8:
                            n_pass += 1
                    elif abs(v2) > 1e-15:
                        rel_diff = abs(v1 - v2) / abs(v2)
                        if rel_diff < 1e-8:
                            n_pass += 1
                except Exception:
                    continue
            details['numerical_tests_passed'] = n_pass
            details['numerical_tests_total'] = n_tests
            if n_pass >= 9:
                return VerificationResult(
                    decision=EquivalenceResult.EQUIVALENT,
                    confidence=0.92, method="numerical_equivalence", details=details)
            elif n_pass <= 2:
                return VerificationResult(
                    decision=EquivalenceResult.NOT_EQUIVALENT,
                    confidence=0.85, method="numerical_nonequivalence", details=details)
        except Exception:
            pass
        return None

    def _fuzzy_string_comparison(self, s1, s2, details):
        c1 = re.sub(r'\s+', '', s1)
        c2 = re.sub(r'\s+', '', s2)
        if c1 == c2:
            return VerificationResult(
                decision=EquivalenceResult.EQUIVALENT,
                confidence=0.85, method="fuzzy_string_exact", details=details)
        if sorted(c1) == sorted(c2) and len(c1) == len(c2) and len(c1) > 3:
            return VerificationResult(
                decision=EquivalenceResult.EQUIVALENT,
                confidence=0.60, method="fuzzy_char_sort", details=details)
        if len(c1) > 5 and len(c2) > 5:
            set1 = set(c1)
            set2 = set(c2)
            overlap = len(set1 & set2) / max(len(set1 | set2), 1)
            if overlap < 0.3:
                return VerificationResult(
                    decision=EquivalenceResult.NOT_EQUIVALENT,
                    confidence=0.70, method="fuzzy_low_overlap", details=details)
        return None
