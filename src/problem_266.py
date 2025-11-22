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