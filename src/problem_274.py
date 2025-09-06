# Problem: https://projecteuler.net/problem=274
from sympy.ntheory import primerange
from tqdm import tqdm

def main():
    """
    Purpose
    Solves Project Euler problem 274 by computing the sum of divisibility multipliers
    for all primes less than 10^7 that are coprime to 10.

    Args
    None

    Returns
    None

    Method / Math Rationale
    The divisibility multiplier m for each qualifying prime p is the modular inverse
    of 10 modulo p, since this satisfies the condition that n is divisible by p if
    and only if the transformed number (n // 10) + (n % 10) * m is divisible by p.
    The function uses sympy's primerange to generate primes from 3 to 10^7 - 1,
    skips p=5, computes the inverse using Python's built-in pow function, and
    accumulates the sum.

    Complexity
    O(N log log N) for generating primes up to N=10^7 using the sieve, plus O(π(N))
    for iterating over approximately 664,579 primes, which is negligible.

    References
    https://projecteuler.net/problem=274
    """
    N: int = 10**7
    total: int = 0
    for p in tqdm(primerange(3, N)):
        if p == 5:
            continue
        m: int = pow(10, -1, p)
        total += m
    print(total)

if __name__ == "__main__":
    main()