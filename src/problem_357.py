# Problem: https://projecteuler.net/problem=357
import math
import numpy as np
from numba import jit
from tqdm import tqdm

@jit(nopython=True)
def is_valid(n: int, isprime: np.ndarray) -> bool:
    sqrt = int(math.sqrt(n)) + 1
    for d in range(1, sqrt):
        if n % d == 0:
            sum_div = d + n // d
            if sum_div >= len(isprime) or not isprime[sum_div]:
                return False
    return True

def main():
    """
    Purpose
    -------
    Computes the sum of all positive integers n <= 100,000,000 such that for every divisor d of n,
    d + n/d is prime.

    Method / Math Rationale
    ------------------------
    First, generate a list of primes up to 100,000,000 + 1 using the Sieve of Eratosthenes.
    Then, identify candidates n where n + 1 is prime.
    For each candidate, check if for all divisors d in 1 to sqrt(n), if d divides n, then
    d + n/d is prime. The symmetry ensures checking the pair is covered.
    Since the condition implies n is square-free and has specific properties, but we check directly.

    Complexity
    ----------
    Time: O(N log log N + pi(N) * sqrt(N)) where N=1e8, approximately 5e10 operations, but
    optimized with early exits and JIT.
    Space: O(N) for the prime sieve.

    References
    ----------
    https://projecteuler.net/problem=357
    """
    LIMIT = 100000000
    isprime = np.full(LIMIT + 2, True, dtype=bool)
    isprime[0] = isprime[1] = False
    for i in range(2, int(math.sqrt(LIMIT + 1)) + 1):
        if isprime[i]:
            isprime[i * i : LIMIT + 2 : i] = False
    candidates = np.where(isprime[2:])[0] + 1
    total = 0
    for n in tqdm(candidates):
        if is_valid(n, isprime):
            total += n
    print(total)

if __name__ == "__main__":
    main()