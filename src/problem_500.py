# Problem: https://projecteuler.net/problem=500
import heapq
from tqdm import tqdm

def generate_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

class Term:
    def __init__(self, p, m):
        self.p = p
        self.m = m

    def __lt__(self, other):
        p1 = self.p
        m1 = self.m
        p2 = other.p
        m2 = other.m
        if m1 == m2:
            return p1 < p2
        d = abs(m1 - m2)
        if d >= 5:
            return m1 < m2
        exp = 1 << d
        if m1 > m2:
            power = p1 ** exp
            return power < p2
        else:
            power = p2 ** exp
            return power > p1

def mod_pow(base, level, mod):
    result = base % mod
    for _ in range(level):
        result = (result * result) % mod
    return result

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 500: Find the smallest number with exactly 2^500500 divisors, modulo 500500507.

    Method / Math Rationale
    -----------------------
    Uses a greedy algorithm with a priority queue to build the number by repeatedly choosing the smallest multiplier
    that doubles the number of divisors. Each multiplier is either introducing a new prime or extending an existing
    one's exponent. Exponents are of the form 2^k - 1 for some k.
    The result is computed modulo 500500507 using modular exponentiation.

    Complexity
    -----------------------
    O(N log P + S) where N=500500, P=number of primes used (~N in worst case but less), S=sieve time O(L log log L)
    with L~8e6.

    References
    ----------
    https://projecteuler.net/problem=500
    """
    MOD = 500500507
    N = 500500
    LIMIT = 8000000
    primes = generate_primes(LIMIT)
    heap = []
    heapq.heappush(heap, Term(primes[0], 0))
    result = 1
    prime_idx = 0
    for _ in tqdm(range(N)):
        term = heapq.heappop(heap)
        p = term.p
        m = term.m
        multiplier = mod_pow(p, m, MOD)
        result = (result * multiplier) % MOD
        heapq.heappush(heap, Term(p, m + 1))
        if m == 0:
            prime_idx += 1
            if prime_idx < len(primes):
                heapq.heappush(heap, Term(primes[prime_idx], 0))
    print(result)

if __name__ == "__main__":
    main()