# Problem: https://projecteuler.net/problem=266
import math
from bisect import bisect_right
from typing import List
from tqdm import tqdm
from sympy.ntheory import primerange


def gen_subset_products(prime_group: List[int]) -> List[int]:
    subset_products: List[int] = [1]
    for prime in prime_group:
        subset_products += [value * prime for value in subset_products]
    return subset_products


def main() -> None:
    """
    Purpose: Compute the required maximal divisor m of the constructed integer (product of specified
    primes) not exceeding its square root and output m modulo 10^16.

    Args: None

    Returns: None; prints the result modulo 10^16.

    Method / Math Rationale: Let N be the product of the chosen primes. Any divisor m of N not
    exceeding sqrt(N) is a product of a subset of those primes. Splitting the prime set into two
    halves enables a meet-in-the-middle search: precompute all subset products for each half
    (lists A and B). For each a in A, we need the largest b in B such that a * b <= sqrt(N). This
    inequality is equivalent to b^2 <= N / a^2, hence b <= floor(sqrt(floor(N / a^2))). Since b
    is integral, using floor(N / a^2) preserves correctness. Sorting the second list permits
    binary search (bisect_right) to extract the optimal b for each a, guaranteeing the global
    optimum under the constraint. The approach is exponential in half the number of primes,
    a standard meet-in-the-middle optimization over naive full enumeration.

    Complexity: Let k be the number of primes. Time: O(2^(k/2) * k + 2^(k/2) log 2^(k/2)) dominated
    by subset generation and per-element binary searches. Space: O(2^(k/2)) for stored subset
    products of one half.

    References: https://projecteuler.net/problem=266; meet-in-the-middle subset product optimization;
    inequality transformation b <= sqrt(N)/a <=> b^2 <= N / a^2.
    """
    primes = list(primerange(2, 190))
    full_product = 1
    for prime in primes:
        full_product *= prime

    half = len(primes) // 2
    group_a = primes[:half]
    group_b = primes[half:]

    subset_products_a = gen_subset_products(group_a)
    subset_products_b = gen_subset_products(group_b)
    subset_products_b.sort()

    best_product = 0
    target = full_product
    for prod_a in tqdm(subset_products_a):
        prod_a_sq = prod_a * prod_a
        if prod_a_sq > target:
            continue
        quotient = target // prod_a_sq
        limit_b = math.isqrt(quotient)
        idx = bisect_right(subset_products_b, limit_b)
        if idx == 0:
            continue
        prod_b = subset_products_b[idx - 1]
        candidate = prod_a * prod_b
        if candidate > best_product:
            best_product = candidate

    print(best_product % (10 ** 16))


if __name__ == "__main__":
    main()