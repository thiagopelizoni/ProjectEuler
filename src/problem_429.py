# Problem: https://projecteuler.net/problem=429
import numpy as np
from tqdm import tqdm

def get_primes(n):
    if n < 2:
        return []
    sieve = np.ones(n + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.nonzero(sieve)[0].tolist()

def exponent(p, n):
    count = 0
    power = p
    while power <= n:
        count += n // power
        if power > n // p:
            break
        power *= p
    return count

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 429: compute the sum of squares of unitary divisors of 100000000! modulo 1000000009.
    Parameters: None
    Returns: None (prints the result)

    Method / Math Rationale
    -----------------------
    The sum S(n) for n = N! is product over primes p <= N of (1 + p^{2 * v_p(N!)}), where v_p is the exponent in N!.
    v_p = sum floor(N / p^k) for k>=1.
    Compute using sieve for primes, loop to compute exponents, modular exponentiation, and accumulate product modulo MOD.

    Complexity
    ----------
    Time: O(N log log N) for sieve + O(pi(N) * log N) for exponents and modular pow, where pi(10^8) ≈ 5.76e6, log N ≈ 27.
    Space: O(N) for sieve.

    References
    ----------
    https://projecteuler.net/problem=429
    """
    N = 100000000
    MOD = 1000000009
    primes = get_primes(N)
    result = 1
    for p in tqdm(primes):
        a = exponent(p, N)
        term = (1 + pow(p, 2 * a, MOD)) % MOD
        result = (result * term) % MOD
    print(result)

if __name__ == "__main__":
    main()