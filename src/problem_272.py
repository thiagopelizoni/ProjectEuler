# Problem: https://projecteuler.net/problem=272

from concurrent.futures import ProcessPoolExecutor
from math import sqrt
from os import cpu_count
from tqdm import tqdm
from typing import List

import numba
from numba import jit
import numpy as np

def generate_p_primes(limit: int) -> List[int]:
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(7, limit + 1) if is_prime[i] and i % 3 == 1]

@jit(nopython=True)
def a_recurse(index: int, current_a: int, primes: np.ndarray, M: int,
              S: np.ndarray) -> int:
    if index == primes.shape[0]:
        return current_a * S[M // current_a] if current_a <= M else 0
    total = 0
    p = primes[index]
    new_a = current_a
    while new_a <= M:
        total += a_recurse(index + 1, new_a, primes, M, S)
        if p > M // new_a:
            break
        new_a *= p
    return total

@jit(nopython=True)
def recurse_helper(curr_index: int, current_count: int, prod: int,
                   current_s: List[int], p: np.ndarray, L: int,
                   S: np.ndarray, is_case1: bool) -> int:
    max_count = 5 if is_case1 else 4
    if current_count == max_count:
        if is_case1:
            primes = np.array(current_s, dtype=np.int64)
            M = L // prod
            return prod * a_recurse(0, 1, primes, M, S)
        else:
            primes = np.array(current_s + [3], dtype=np.int64)
            new_prod = prod * 9
            M = L // new_prod
            return new_prod * a_recurse(0, 1, primes, M, S)
    total = 0
    for j in range(curr_index + 1, p.shape[0]):
        new_prod = prod * p[j]
        if new_prod > L:
            break
        total += recurse_helper(j, current_count + 1, new_prod,
                                current_s + [p[j]], p, L, S, is_case1)
    return total

def recurse_case(start: int, end: int, p: np.ndarray, L: int,
                 S: np.ndarray, is_case1: bool) -> int:
    total = 0
    for i in tqdm(range(start, end)):
        total += recurse_helper(i, 1, p[i], [p[i]], p, L, S, is_case1)
    return total

def main() -> None:
    """
    Purpose
    Computes the sum of positive n <= 10^11 with C(n) = 242, where C(n) is the
    number of integers 1 < x < n with x^3 ≡ 1 mod n.

    Method / Math Rationale
    Enumerates increasing combinations of primes ≡1 mod 3 using recursion with
    product pruning. For case1 (5 such primes): prod = product of them, sum
    over additional e>=0 for each: prod * a * sum b <= L/(prod*a) where b has
    only primes 2, ≡2 mod 3 (any e), 3^{0 or 1}. For case2 (4 such primes,
    plus 3^{e>=2}): prod = product of 4 * 9, sum over additional e>=0 for the
    4 and 3: prod * a * sum b <= L/(prod*a) where b has only 2, ≡2 mod 3 (any
    e), no 3.

    Complexity
    Time: O(number of combinations * average log(M/p) per prime for exponents),
    ~ seconds to minutes with Numba JIT and parallelism; Space: O(MAX_M)

    References
    https://projecteuler.net/problem=272
    """
    L: int = 10**11
    MAX_M: int = 10**6
    LIMIT: int = 10**7
    p_list: List[int] = generate_p_primes(LIMIT)
    p: np.ndarray = np.array(p_list, dtype=np.int64)

    def compute_S(mark_threes: bool) -> np.ndarray:
        is_good = [True] * (MAX_M + 1)
        is_good[0] = False
        for bp in p_list:
            if bp > MAX_M:
                break
            for j in range(bp, MAX_M + 1, bp):
                is_good[j] = False
        if mark_threes:
            for j in range(3, MAX_M + 1, 3):
                is_good[j] = False
        else:
            for j in range(9, MAX_M + 1, 9):
                is_good[j] = False
        cum = [0] * (MAX_M + 1)
        for b in range(1, MAX_M + 1):
            cum[b] = cum[b - 1] + (b if is_good[b] else 0)
        return np.array(cum, dtype=np.int64)

    S_with3: np.ndarray = compute_S(False)
    S_no3: np.ndarray = compute_S(True)

    num_cpus: int = cpu_count() or 4
    chunk_size: int = len(p_list) // num_cpus + 1
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(recurse_case, i * chunk_size,
                                   min((i + 1) * chunk_size, len(p_list)),
                                   p, L, S_with3, True)
                   for i in range(num_cpus)]
        case1_sum: int = sum(f.result() for f in futures)
        futures = [executor.submit(recurse_case, i * chunk_size,
                                   min((i + 1) * chunk_size, len(p_list)),
                                   p, L, S_no3, False)
                   for i in range(num_cpus)]
        case2_sum: int = sum(f.result() for f in futures)
    print(case1_sum + case2_sum)

if __name__ == "__main__":
    main()