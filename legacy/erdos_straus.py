import sys, time
sys.path.insert(0, '/home/claude/geo_verify')
from math import gcd
import sympy as sp
from sympy import divisors

# ---------------------------------------------------------------
# Erdos-Straus conjecture (OPEN, 1948):
#   for every integer n >= 2,  4/n = 1/x + 1/y + 1/z  has a positive-integer solution.
#
# Reasoning that shrinks the search (this is the "reason about it" part):
#  (1) Multiplicativity: a solution for a divisor d of n lifts to n
#      (4/(d*m) = 1/(m*x)+1/(m*y)+1/(m*z)). => only PRIMES need checking.
#  (2) Standard identities solve every residue class mod 840 EXCEPT the six
#      classes r in {1,121,169,289,361,529} (the squares coprime to 840).
#      => only primes p with (p mod 840) in that set are "hard".
#  A single n with NO solution (within a generous denominator cap) would be a
#  candidate counterexample -> flagged for scrutiny.
# ---------------------------------------------------------------

HARD = {1, 121, 169, 289, 361, 529}

def solve_es(n, xwindow=400):
    """Return (x,y,z) with 4/n = 1/x+1/y+1/z, or None found in the x-window.

    For each x, 1/y+1/z = p/q with p=4x-n, q=nx.  Writing A=py-q, B=pz-q gives
    A*B = q^2, so y,z come from factor pairs of q^2 (fast) instead of scanning.
    """
    xstart = n // 4 + 1
    for x in range(xstart, xstart + xwindow):
        p = 4 * x - n
        if p <= 0:
            continue
        q = n * x
        g = gcd(p, q); p2, q2 = p // g, q // g
        q2sq = q2 * q2
        # iterate divisors A of q2^2 with A <= q2 (A<=B); need (q2+A) % p2 == 0
        for A in divisors(q2sq):
            if A > q2:
                break
            if (q2 + A) % p2 == 0:
                B = q2sq // A
                y = (q2 + A) // p2
                z = (q2 + B) // p2
                if y > 0 and z > 0:
                    return (x, y, z)
    return None

def verify_up_to(N, hard_only=True, time_budget=90):
    t0 = time.time()
    checked = 0
    hardest = []
    failures = []
    reached = 1
    for n in sp.primerange(2, N + 1):
        if hard_only and (n % 840) not in HARD:
            reached = n
            continue
        sol = solve_es(n)
        checked += 1
        if sol is None:
            failures.append(n)
        reached = n
        if time.time() - t0 > time_budget:
            break
    return checked, failures, reached, time.time() - t0

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    # sanity: verify a couple of known hard primes solve
    for n in [1009, 2017, 3361]:
        print(f"  4/{n} = ", solve_es(n))
    print(f"\nVerifying Erdos-Straus for HARD-residue primes up to {N} ...")
    checked, failures, reached, dt = verify_up_to(N, hard_only=True)
    print(f"  hard-residue primes checked: {checked}")
    print(f"  reached n = {reached} in {dt:.1f}s")
    print(f"  counterexamples (primes with NO decomposition): {failures if failures else 'NONE'}")
