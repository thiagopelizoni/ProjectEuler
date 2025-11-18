# Problem: https://projecteuler.net/problem=510
import math
from tqdm import tqdm

def triangle(n):
    return n * (n + 1) // 2

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 510 by computing S(10^9), where S(n) is the sum of r_A + r_B + r_C over all
    integer triples (r_A, r_B, r_C) with 0 < r_A <= r_B <= n that satisfy the tangent circles conditions.
    
    Method / Math Rationale
    ----------------------
    The valid radii r_A, r_B, r_C are perfect squares. Let sqrt(r_B) = a, sqrt(r_A) = b with a >= b >= 1
    integers. Then r_C = [a b / (a + b)]^2 must be integer, i.e., (a + b)^2 divides a^2 b^2.
    Enumerate all such a, b where this holds and the triple is primitive (gcd(r_A, r_B, r_C) = 1).
    For each primitive triple, compute the contribution from its multiples k * (r_A, r_B, r_C) where
    k r_B <= 10^9, adding (r_A + r_B + r_C) * sum_{k=1}^M k = (r_A + r_B + r_C) * M(M+1)/2
    where M = floor(10^9 / r_B).

    Complexity
    ----------
    O(sqrt(n)^2) = O(n) time due to nested loops over a and b up to sqrt(n) ≈ 31622, resulting in about
    5e8 iterations, feasible with optimized operations.

    References
    ----------
    https://projecteuler.net/problem=510
    Adapted from C++ solution at https://euler.stephan-brumme.com/510/
    """
    n = 10**9
    result = 0
    max_a = math.isqrt(n)
    for a in tqdm(range(1, max_a + 1)):
        a2 = a * a
        for b in range(1, a + 1):
            b2 = b * b
            numerator = a2 * b2
            denominator = (a + b) * (a + b)
            if numerator % denominator != 0:
                continue
            c2 = numerator // denominator
            g = math.gcd(math.gcd(a2, b2), c2)
            if g == 1:
                M = n // a2
                sum_radii = a2 + b2 + c2
                contrib = sum_radii * triangle(M)
                result += contrib
    print(result)

if __name__ == "__main__":
    main()