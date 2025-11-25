# Problem: https://projecteuler.net/problem=521
import numpy as np
from numba import njit

@njit(fastmath=True, cache=True)
def solve_problem_521(limit: int, mod: int) -> int:
    sqrt_limit = int(limit ** 0.5)
    is_prime = np.ones(sqrt_limit + 1, dtype=np.bool_)
    is_prime[0] = is_prime[1] = False
    primes = np.empty(sqrt_limit, dtype=np.int64)
    p_count = 0

    for i in range(2, sqrt_limit + 1):
        if is_prime[i]:
            primes[p_count] = i
            p_count += 1
            for j in range(i * i, sqrt_limit + 1, i):
                is_prime[j] = False

    primes = primes[:p_count]

    vals = np.empty(2 * sqrt_limit + 2, dtype=np.int64)
    count_vals = 0
    i = 1
    while i <= limit:
        val = limit // i
        vals[count_vals] = val
        count_vals += 1
        i = (limit // val) + 1

    vals = vals[:count_vals]

    id1 = np.empty(sqrt_limit + 1, dtype=np.int32)
    id2 = np.empty(sqrt_limit + 1, dtype=np.int32)

    for idx, v in enumerate(vals):
        if v <= sqrt_limit:
            id1[v] = idx
        else:
            id2[limit // v] = idx

    S1 = np.empty(count_vals, dtype=np.int64)
    S2 = np.empty(count_vals, dtype=np.int64)

    for i in range(count_vals):
        v = vals[i]
        S1[i] = v - 1
        if v % 2 == 0:
            a = v // 2
            b = v + 1
        else:
            a = v
            b = (v + 1) // 2
        term = (a % mod) * (b % mod)
        S2[i] = (term - 1) % mod

    ans_composites = 0

    for p in primes:
        p2 = p * p
        if p2 > limit:
            break
        if p - 1 <= sqrt_limit:
            idx_p_prev = id1[p - 1]
        else:
            idx_p_prev = id2[limit // (p - 1)]
        sp_cnt = S1[idx_p_prev]
        sp_sum = S2[idx_p_prev]
        for j in range(count_vals):
            v = vals[j]
            if v < p2:
                break
            div_v = v // p
            if div_v <= sqrt_limit:
                k = id1[div_v]
            else:
                k = id2[limit // div_v]
            count_removed = S1[k] - sp_cnt
            sum_removed = S2[k] - sp_sum
            S1[j] -= count_removed
            term_sub = (p * (sum_removed % mod)) % mod
            S2[j] = (S2[j] - term_sub + mod) % mod
            if v == limit:
                contrib = (p * (count_removed % mod)) % mod
                ans_composites = (ans_composites + contrib) % mod

    ans_primes = S2[0]
    total_ans = (ans_composites + ans_primes) % mod
    return total_ans

def main():
    limit = 10**12
    mod = 10**9
    result = solve_problem_521(limit, mod)
    print(result)

if __name__ == "__main__":
    main()