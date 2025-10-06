# Problem: https://projecteuler.net/problem=398
from tqdm import tqdm
import sys

def binom_ratio(a, r, denom_base):
    if a < r or a < 0:
        return 0.0
    prod = 1.0
    for i in range(r):
        num = a - i
        den = denom_base - i
        if num <= 0:
            return 0.0
        prod *= num / den
    return prod

def main():
    """
    Purpose
    -------
    Computes the expected length of the second-shortest segment for the rope cutting problem in Project Euler 398.

    Method / Math Rationale
    -----------------------
    Uses the tail sum for expectation E[X] = sum_{k>=1} P(X >= k), where X is the second-shortest segment length.
    P(X >= k) is calculated as the probability all segments >=k plus the probability exactly one segment <k
    and the rest >=k, using binomial coefficient ratios computed via products.

    Complexity
    ----------
    O( max_k * m ) where max_k ~ n/m, m=100, n=10^7, so O(10^5 * 100) = O(10^7), acceptable.

    References
    ----------
    https://projecteuler.net/problem=398
    """
    n = 10000000
    m = 100
    denom_base = n - 1
    max_k = n // (m - 1) + 2
    expected = 0.0
    for k in tqdm(range(1, max_k)):
        p = 0.0
        # P(all >= k)
        km1 = k - 1
        s = n - m * km1
        if s >= m:
            x = s - 1
            if x >= m - 1:
                p_all = binom_ratio(x, m - 1, denom_base)
                p += p_all
        # P(exactly one < k)
        b = n - (m - 1) * km1 - 1
        high = b - 1
        low = b - (k - 1)
        p_exact = 0.0
        if high >= m - 2 >= 0:
            c_high = binom_ratio(high + 1, m - 1, denom_base)
            c_low = binom_ratio(low, m - 1, denom_base) if low >= m - 1 else 0.0
            p_exact = m * (c_high - c_low)
        p += p_exact
        if p < 1e-12:
            break
        expected += p
    print(f"{expected:.5f}")

if __name__ == "__main__":
    main()