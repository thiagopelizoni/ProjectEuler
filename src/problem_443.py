# Problem: https://projecteuler.net/problem=443
from math import gcd
from sympy.ntheory import factorint
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Computes g(10^15) where g is the GCD sequence defined in the problem.

    Method / Math Rationale
    -----------------------
    Uses the offset b(n) = g(n) - n, which stays constant between jumps where gcd >1.
    Jumps to the next n where gcd(n, b-1) >1 by finding the minimal next multiple of
    primes dividing (b-1).
    At each jump, updates b += gcd -1.
    This avoids iterating over all n.

    Complexity
    ----------
    O(J * F) where J is number of jumps (~ few hundred), F is time to factorize numbers
    up to ~10^15 (~ fast with sympy).

    References
    ----------
    https://projecteuler.net/problem=443
    """
    N = 10**15
    n = 4
    b = 9
    pbar = tqdm(desc="Processing jumps", unit="jump")
    while n < N:
        s = b - 1
        primes = list(factorint(s).keys())
        if not primes:
            break
        min_m = float('inf')
        for p in primes:
            start = n + 1
            remainder = start % p
            if remainder == 0:
                m_p = start
            else:
                m_p = start + (p - remainder)
            min_m = min(min_m, m_p)
        m = min_m
        if m > N:
            break
        d = gcd(m, s)
        b += d - 1
        n = m
        pbar.update(1)
    pbar.close()
    g = N + b
    print(g)

if __name__ == "__main__":
    main()