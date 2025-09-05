# Problem: https://projecteuler.net/problem=271
# Problem: https://projecteuler.net/problem=271

from itertools import product
from tqdm import tqdm
from typing import List

def main() -> None:
    """
    Purpose
    Computes S(13082761331670030), the sum of integers x where 1 < x < n
    and x^3 ≡ 1 mod n.

    Method / Math Rationale
    Factors n as the product of the first 14 primes. Identifies primes with
    1 or 3 solutions to x^3 ≡ 1 mod p. Fixes x ≡ 1 mod m1 (product of
    single-solution primes). Enumerates all 3^6 = 729 combinations of
    residues for the 6 primes with 3 solutions, computes c mod m2 using CRT,
    then solves x ≡ 1 mod m1, x ≡ c mod m2 explicitly. Sums all such x and
    subtracts 1.

    Complexity
    Time: O(729 * 6) constant time, Space: O(1)

    References
    https://projecteuler.net/problem=271
    """
    single_primes: List[int] = [2, 3, 5, 11, 17, 23, 29, 41]
    m1: int = 1
    for p in single_primes:
        m1 *= p
    triple_primes: List[int] = [7, 13, 19, 31, 37, 43]
    m2: int = 1
    for p in triple_primes:
        m2 *= p
    sols: List[List[int]] = [[1, 2, 4], [1, 3, 9], [1, 7, 11],
                             [1, 5, 25], [1, 10, 26], [1, 6, 36]]
    inv_m1: int = pow(m1, -1, m2)
    total_sum: int = 0
    for combo in tqdm(product(*sols)):
        c: int = 0
        for i in range(len(triple_primes)):
            mod: int = triple_primes[i]
            rem: int = combo[i]
            p: int = m2 // mod
            inv: int = pow(p, -1, mod)
            c += rem * inv * p
        c %= m2
        diff: int = (c - 1) % m2
        t: int = (diff * inv_m1) % m2
        x: int = 1 + m1 * t
        total_sum += x
    print(total_sum - 1)

if __name__ == "__main__":
    main()