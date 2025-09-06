# Problem: https://projecteuler.net/problem=279
from math import gcd
from tqdm import tqdm
from typing import List

def count_60(limit: int) -> int:
    last: int = int((limit * 3 / 2) ** 0.5) + 1
    result: int = 0
    for m in tqdm(range(2, last + 1)):
        for n in range(1, m // 2 + 1):
            if gcd(m, n) != 1:
                continue
            a: int = m * m - m * n + n * n
            b: int = 2 * m * n - n * n
            c: int = m * m - n * n
            peri: int = a + b + c
            if a % 3 == 0 and b % 3 == 0 and c % 3 == 0:
                peri //= 3
            if peri > limit:
                continue
            num_multiples: int = limit // peri
            result += num_multiples
    return result

def count_90(limit: int) -> int:
    last: int = int((limit / 2) ** 0.5) + 1
    result: int = 0
    for m in tqdm(range(2, last + 1)):
        n_start: int = 1 if m % 2 == 0 else 2
        for n in range(n_start, m, 2):
            if gcd(m, n) != 1:
                continue
            a: int = m * m - n * n
            b: int = 2 * m * n
            c: int = m * m + n * n
            peri: int = a + b + c
            if peri > limit:
                break
            num_multiples: int = limit // peri
            result += num_multiples
    return result

def count_120(limit: int) -> int:
    last: int = int((limit * 3 / 2) ** 0.5) + 1
    result: int = 0
    for m in tqdm(range(2, last + 1)):
        for n in range(1, m // 2 + 1):
            if gcd(m, n) != 1:
                continue
            a: int = m * m + m * n + n * n
            b: int = 2 * m * n + n * n
            c: int = m * m - n * n
            if b > c:
                continue
            peri: int = a + b + c
            if a % 3 == 0 and b % 3 == 0 and c % 3 == 0:
                peri //= 3
            if peri > limit:
                continue
            num_multiples: int = limit // peri
            result += num_multiples
    return result

def main() -> None:
    """Purpose:
    Computes the number of integer-sided triangles with perimeter <= 10^8 having
    at least one integer degree angle.

    Method / Math Rationale:
    By Niven's theorem, the only possible integer angles in such triangles are
    60°, 90°, or 120°. The sets of triangles with these angles are disjoint.
    Generates base triples for each angle using parametric formulas for
    Eisenstein (60° and 120°) and Pythagorean (90°) triples, adjusts for common
    divisors of 3 where applicable, and sums the number of multiples with
    perimeter <= limit.

    Complexity:
    Time: O(N), Space: O(1)

    References:
    https://projecteuler.net/problem=279
    """
    limit: int = 100000000
    total: int = count_60(limit) + count_90(limit) + count_120(limit)
    print(total)

if __name__ == "__main__":
    main()