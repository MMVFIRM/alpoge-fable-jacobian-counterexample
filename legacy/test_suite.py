"""
GeoVerify Test Suite
"""
import sys
sys.path.insert(0, '/home/claude/geo_verify')
from core import GeoVerifier, EquivalenceResult
import json
from dataclasses import dataclass
from typing import List

@dataclass
class TestCase:
    name: str
    reference: str
    prediction: str
    expected: EquivalenceResult
    category: str
    description: str

def build_test_suite() -> List[TestCase]:
    cases = []
    cases.append(TestCase(
        name="paper_case1_pdf_joint",
        reference=r"\frac{1}{2\pi} \cdot \frac{1}{1+v^2} e^{-\frac{u}{2}}",
        prediction=r"\frac{1}{2\pi(v^2 + 1)} e^{-u/2}",
        expected=EquivalenceResult.EQUIVALENT, category="paper_case_1",
        description="Different ordering of v^2, constant 2pi combined"))
    cases.append(TestCase(
        name="paper_case2_symbol_order",
        reference=r"-4ni", prediction=r"-4in",
        expected=EquivalenceResult.EQUIVALENT, category="paper_case_2",
        description="Order of symbols i and n reversed"))
    cases.append(TestCase(
        name="paper_case3_generating_function",
        reference=r"\frac{2t^2}{1 - t^2} \prod_{n \geq 1} \frac{1}{1 - t^n}",
        prediction=r"\frac{2t^2}{1 - t^2} \prod_{m=1}^{\infty} \frac{1}{1 - t^m}",
        expected=EquivalenceResult.EQUIVALENT, category="paper_case_3",
        description="Different variable symbols (n vs m), different product notation"))
    cases.append(TestCase(
        name="commutative_addition", reference=r"a + b + c", prediction=r"c + a + b",
        expected=EquivalenceResult.EQUIVALENT, category="reorder",
        description="Simple commutative reordering of addition"))
    cases.append(TestCase(
        name="commutative_multiplication", reference=r"x y z", prediction=r"z x y",
        expected=EquivalenceResult.EQUIVALENT, category="reorder",
        description="Commutative reordering of multiplication"))
    cases.append(TestCase(
        name="fraction_reorder", reference=r"\frac{a^2 + b^2}{c + d}",
        prediction=r"\frac{b^2 + a^2}{d + c}",
        expected=EquivalenceResult.EQUIVALENT, category="reorder",
        description="Reordering within numerator and denominator"))
    cases.append(TestCase(
        name="complex_reorder",
        reference=r"\frac{1}{|G|} \left(2 + \sum_{x \in G, x \neq 1} \text{Re}(\chi(x))\right)",
        prediction=r"\frac{1}{|G|} \left(\sum_{x \in G, x \neq 1} \text{Re}(\chi(x)) + 2\right)",
        expected=EquivalenceResult.EQUIVALENT, category="reorder",
        description="The motivating example from the paper abstract"))
    cases.append(TestCase(
        name="dummy_var_rename_sum", reference=r"\sum_{k=0}^{n} \binom{n}{k} x^k",
        prediction=r"\sum_{j=0}^{n} \binom{n}{j} x^j",
        expected=EquivalenceResult.EQUIVALENT, category="rename",
        description="Dummy variable k renamed to j in summation"))
    cases.append(TestCase(
        name="dummy_var_rename_integral", reference=r"\int_0^1 f(t) dt",
        prediction=r"\int_0^1 f(s) ds",
        expected=EquivalenceResult.EQUIVALENT, category="rename",
        description="Integration variable t renamed to s"))
    cases.append(TestCase(
        name="exp_notation", reference=r"e^{-x^2/2}", prediction=r"\exp(-x^2/2)",
        expected=EquivalenceResult.EQUIVALENT, category="notation",
        description="e^{...} vs exp(...)"))
    cases.append(TestCase(
        name="fraction_vs_division", reference=r"\frac{x+1}{x-1}", prediction=r"(x+1)/(x-1)",
        expected=EquivalenceResult.EQUIVALENT, category="notation",
        description="frac vs ()/() notation"))
    cases.append(TestCase(
        name="sqrt_vs_power", reference=r"\sqrt{x}", prediction=r"x^{1/2}",
        expected=EquivalenceResult.EQUIVALENT, category="notation",
        description="Square root vs power 1/2"))
    cases.append(TestCase(
        name="abs_notation", reference=r"|x|", prediction=r"\lvert x \rvert",
        expected=EquivalenceResult.EQUIVALENT, category="notation",
        description="Different absolute value notation"))
    cases.append(TestCase(
        name="algebraic_expand", reference=r"(x+1)^2", prediction=r"x^2 + 2x + 1",
        expected=EquivalenceResult.EQUIVALENT, category="algebraic",
        description="Factored vs expanded form"))
    cases.append(TestCase(
        name="algebraic_cancel", reference=r"\frac{x^2 - 1}{x - 1}", prediction=r"x + 1",
        expected=EquivalenceResult.EQUIVALENT, category="algebraic",
        description="Fraction that simplifies via cancellation"))
    cases.append(TestCase(
        name="trig_identity", reference=r"\sin^2(x) + \cos^2(x)", prediction=r"1",
        expected=EquivalenceResult.EQUIVALENT, category="algebraic",
        description="Pythagorean identity"))
    cases.append(TestCase(
        name="algebraic_factor", reference=r"x^3 - x", prediction=r"x(x-1)(x+1)",
        expected=EquivalenceResult.EQUIVALENT, category="algebraic",
        description="Expanded vs factored polynomial"))
    cases.append(TestCase(
        name="physics_force", reference=r"\frac{Q^2}{32\pi \epsilon_0 R^2}",
        prediction=r"\frac{Q^2}{32 \pi R^2 \epsilon_0}",
        expected=EquivalenceResult.EQUIVALENT, category="physics",
        description="Reordering of constants in denominator"))
    cases.append(TestCase(
        name="physics_potential", reference=r"-\frac{q^2 E^2}{2m\omega^2}",
        prediction=r"-\frac{E^2 q^2}{2 \omega^2 m}",
        expected=EquivalenceResult.EQUIVALENT, category="physics",
        description="Reordering in physics expression"))
    cases.append(TestCase(
        name="different_sign", reference=r"x + 1", prediction=r"x - 1",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Different sign"))
    cases.append(TestCase(
        name="different_exponent", reference=r"x^2", prediction=r"x^3",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Different exponent"))
    cases.append(TestCase(
        name="different_coefficient", reference=r"2x + 3", prediction=r"3x + 2",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Different coefficients"))
    cases.append(TestCase(
        name="different_function", reference=r"\sin(x)", prediction=r"\cos(x)",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Different trig function"))
    cases.append(TestCase(
        name="missing_term", reference=r"x^2 + x + 1", prediction=r"x^2 + 1",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Missing linear term"))
    cases.append(TestCase(
        name="different_fraction", reference=r"\frac{1}{2\pi}", prediction=r"\frac{1}{4\pi}",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Different constant in fraction"))
    cases.append(TestCase(
        name="close_but_wrong", reference=r"\frac{x}{x+1}", prediction=r"\frac{x}{x-1}",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Similar structure, different sign in denominator"))
    cases.append(TestCase(
        name="off_by_constant", reference=r"e^{-x}", prediction=r"2 e^{-x}",
        expected=EquivalenceResult.NOT_EQUIVALENT, category="non_equiv",
        description="Off by a multiplicative constant"))
    return cases

def run_tests():
    verifier = GeoVerifier(verbose=True)
    cases = build_test_suite()
    correct = 0
    total = 0
    by_category = {}
    print("=" * 80)
    print("GeoVerify Test Suite")
    print("=" * 80)
    for tc in cases:
        total += 1
        result = verifier.verify(tc.reference, tc.prediction)
        effective_decision = result.decision
        if effective_decision == EquivalenceResult.UNCERTAIN:
            effective_decision = EquivalenceResult.NOT_EQUIVALENT
        is_correct = (effective_decision == tc.expected)
        if is_correct:
            correct += 1
        if tc.category not in by_category:
            by_category[tc.category] = {'correct': 0, 'total': 0}
        by_category[tc.category]['total'] += 1
        if is_correct:
            by_category[tc.category]['correct'] += 1
        status = "OK " if is_correct else "XX "
        print(f"  {status} {tc.name}: expected={tc.expected.value}, got={result.decision.value} (conf={result.confidence:.2f}, method={result.method})")
    print("=" * 80)
    print(f"OVERALL: {correct}/{total} = {100*correct/total:.1f}%")
    print("=" * 80)
    print("By category:")
    for cat, stats in sorted(by_category.items()):
        pct = 100 * stats['correct'] / stats['total']
        print(f"  {cat:20s}: {stats['correct']}/{stats['total']} = {pct:.0f}%")
    return correct, total

if __name__ == "__main__":
    run_tests()
