"""
LaTeX Structural Analyzer (Layer 2.5)
"""
import re
from typing import Optional, List, Tuple, Dict, Set
from dataclasses import dataclass, field

@dataclass
class LaTeXToken:
    type: str
    value: str
    children: List['LaTeXToken'] = field(default_factory=list)
    def __repr__(self):
        if self.children:
            return f"{self.type}({self.value}, [{', '.join(str(c) for c in self.children)}])"
        return f"{self.type}({self.value})"

class LaTeXStructuralAnalyzer:
    BINDING_CONSTRUCTS = {
        r'\sum', r'\prod', r'\int', r'\oint',
        r'\bigcup', r'\bigcap', r'\bigoplus',
        r'\coprod', r'\bigotimes',
    }
    LIMIT_EQUIVALENCES = [
        (r'(\w+)\s*\\ge\s*(\d+)', r'\1=\2', 'lower_bound_equiv'),
        (r'(\w+)\s*\\geq\s*(\d+)', r'\1=\2', 'lower_bound_equiv'),
        (r'(\w+)\s*>=\s*(\d+)', r'\1=\2', 'lower_bound_equiv'),
    ]

    def structural_equivalent(self, latex1: str, latex2: str) -> Tuple[bool, float, str]:
        norm1 = self._structural_normalize(latex1)
        norm2 = self._structural_normalize(latex2)
        if norm1 == norm2:
            return True, 0.95, "structural_normalize_exact"
        alpha1 = self._alpha_normalize(norm1)
        alpha2 = self._alpha_normalize(norm2)
        if alpha1 == alpha2:
            return True, 0.93, "alpha_normalized_exact"
        fp1 = self._structural_fingerprint(alpha1)
        fp2 = self._structural_fingerprint(alpha2)
        if fp1 == fp2:
            return True, 0.88, "structural_fingerprint_match"
        parts_equiv, parts_conf = self._compare_decomposed(norm1, norm2)
        if parts_equiv:
            return True, parts_conf, "decomposed_comparison"
        dist = self._token_edit_distance(alpha1, alpha2)
        max_len = max(len(alpha1), len(alpha2), 1)
        normalized_dist = dist / max_len
        if normalized_dist < 0.05:
            return True, 0.80, f"low_edit_distance({normalized_dist:.3f})"
        elif normalized_dist > 0.5:
            return False, 0.75, f"high_edit_distance({normalized_dist:.3f})"
        return False, 0.40, "structural_inconclusive"

    def _structural_normalize(self, s: str) -> str:
        s = s.strip()
        s = re.sub(
            r'(\\(?:prod|sum|bigcup|bigcap))\s*_\s*\{?\s*(\w+)\s*(?:\\ge(?:q)?|>=)\s*(\d+)\s*\}?',
            r'\1_{\2=\3}^{\\infty}',
            s
        )
        s = re.sub(r'\\infinity', r'\\infty', s)
        s = re.sub(r'_\s*\{', '_{', s)
        s = re.sub(r'\^\s*\{', '^{', s)
        s = re.sub(r'\\limits\s*', '', s)
        s = re.sub(r'\\cdot\s*', '*', s)
        s = re.sub(r'\\times\s*', '*', s)
        s = re.sub(r'\\,\s*d(\w)', r' d\1', s)
        s = re.sub(r'\\mathrm\{d\}', 'd', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    def _alpha_normalize(self, s: str) -> str:
        bound_vars = []
        binding_pattern = re.compile(
            r'(\\(?:sum|prod|int|oint|bigcup|bigcap|coprod|bigoplus|bigotimes))'
            r'\s*_\s*\{?\s*([a-zA-Z])\s*[=\\]'
        )
        for match in binding_pattern.finditer(s):
            var = match.group(2)
            if var not in bound_vars:
                bound_vars.append(var)
        int_var_pattern = re.compile(r'\\int.*?\s+d([a-zA-Z])\b')
        for match in int_var_pattern.finditer(s):
            var = match.group(1)
            if var not in bound_vars:
                bound_vars.append(var)
        result = s
        for i, var in enumerate(bound_vars):
            canonical = f'_BV{i}_'
            result = re.sub(
                r'(?<![a-zA-Z])d' + re.escape(var) + r'(?![a-zA-Z])',
                f'd{canonical}', result)
            result = re.sub(
                r'(?<![a-zA-Z_])' + re.escape(var) + r'(?![a-zA-Z_0-9])',
                canonical, result)
        return result

    def _structural_fingerprint(self, s: str) -> str:
        commands = re.findall(r'\\[a-zA-Z]+', s)
        cmd_seq = ' '.join(commands)
        delims = re.findall(r'[{}()\[\]_^]', s)
        delim_seq = ''.join(delims)
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', s)
        num_seq = ','.join(sorted(numbers))
        ops = re.findall(r'[+\-*/=<>]', s)
        op_seq = ''.join(sorted(ops))
        return f"C:{cmd_seq}|D:{delim_seq}|N:{num_seq}|O:{op_seq}"

    def _compare_decomposed(self, s1: str, s2: str) -> Tuple[bool, float]:
        parts1 = self._split_multiplicative(s1)
        parts2 = self._split_multiplicative(s2)
        if len(parts1) != len(parts2):
            return False, 0.0
        if len(parts1) <= 1:
            return False, 0.0
        matched = 0
        for p1 in parts1:
            an1 = self._alpha_normalize(p1.strip())
            for p2 in parts2:
                an2 = self._alpha_normalize(p2.strip())
                if an1 == an2:
                    matched += 1
                    break
        if matched == len(parts1):
            return True, 0.90
        if matched > 0 and matched >= len(parts1) - 1:
            return True, 0.75
        return False, 0.0

    def _split_multiplicative(self, s: str) -> List[str]:
        parts = []
        depth = 0
        current = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == '{':
                depth += 1
                current.append(c)
            elif c == '}':
                depth -= 1
                current.append(c)
            elif c == ' ' and depth == 0:
                chunk = ''.join(current).strip()
                if chunk:
                    rest = s[i:].strip()
                    is_binding = any(rest.startswith(bc) for bc in
                                   [r'\prod', r'\sum', r'\int', r'\oint'])
                    if is_binding and chunk:
                        parts.append(chunk)
                        current = []
                    else:
                        current.append(c)
                else:
                    current.append(c)
            else:
                current.append(c)
            i += 1
        final = ''.join(current).strip()
        if final:
            parts.append(final)
        return parts if len(parts) > 1 else [s]

    def _token_edit_distance(self, s1: str, s2: str) -> int:
        tokens1 = self._tokenize(s1)
        tokens2 = self._tokenize(s2)
        n, m = len(tokens1), len(tokens2)
        if n == 0:
            return m
        if m == 0:
            return n
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 0 if tokens1[i-1] == tokens2[j-1] else 1
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + cost
                )
        return dp[n][m]

    def _tokenize(self, s: str) -> List[str]:
        tokens = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                j = i + 1
                while j < len(s) and s[j].isalpha():
                    j += 1
                tokens.append(s[i:j])
                i = j
            elif s[i].isdigit() or (s[i] == '.' and i+1 < len(s) and s[i+1].isdigit()):
                j = i
                while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                tokens.append(s[i:j])
                i = j
            elif s[i].isalpha() or s[i] == '_':
                j = i
                while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                    j += 1
                tokens.append(s[i:j])
                i = j
            elif s[i] in ' \t\n':
                i += 1
            else:
                tokens.append(s[i])
                i += 1
        return tokens
