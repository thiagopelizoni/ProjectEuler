# Problem: https://projecteuler.net/problem=311
import numpy as np
import math
from numba import njit, prange

LIMIT = 10_000_000_000
LIMIT_S = LIMIT // 4


@njit(fastmath=True, cache=True)
def get_primes(n):
    is_prime = np.ones(n + 1, dtype=np.bool_)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            is_prime[i * i : n + 1 : i] = False
    return np.nonzero(is_prime)[0]


@njit(parallel=True, fastmath=True)
def solve_biclinic(limit):
    sqrt_limit = int(math.sqrt(limit))
    primes = get_primes(sqrt_limit + 100)

    block_size = 65_536
    num_blocks = (limit + block_size - 1) // block_size

    block_sums = np.zeros(num_blocks, dtype=np.uint64)

    for b in prange(num_blocks):
        start = b * block_size + 1
        end = min((b + 1) * block_size + 1, limit + 1)
        length = end - start

        if length <= 0:
            continue

        nums = np.arange(start, end, dtype=np.uint32)
        d1_counts = np.ones(length, dtype=np.uint32)
        valid = np.ones(length, dtype=np.bool_)

        for p in primes:
            p_sq = p * p
            if p_sq > end:
                break

            rem = start % p
            first_idx = (p - rem) if rem != 0 else 0

            if p == 2:
                for i in range(first_idx, length, p):
                    n = nums[i]
                    while (n & 1) == 0:
                        n >>= 1
                    nums[i] = n
            elif (p & 3) == 1:
                for i in range(first_idx, length, p):
                    n = nums[i]
                    count = 0
                    while n % p == 0:
                        count += 1
                        n //= p
                    nums[i] = n
                    d1_counts[i] *= (count + 1)
            else:
                for i in range(first_idx, length, p):
                    if not valid[i]:
                        continue
                    n = nums[i]
                    count = 0
                    while n % p == 0:
                        count += 1
                        n //= p
                    nums[i] = n
                    if (count & 1):
                        valid[i] = False

        local_total = 0
        for i in range(length):
            if not valid[i]:
                continue

            n = nums[i]
            d1 = d1_counts[i]

            if n > 1:
                if (n & 3) == 1:
                    d1 *= 2
                elif (n & 3) == 3:
                    continue

            S = start + i

            is_dsq = False
            is_sq = False

            root = int(math.sqrt(S))
            if root * root == S:
                is_sq = True

            if (S & 1) == 0:
                half = S >> 1
                root_h = int(math.sqrt(half))
                if root_h * root_h == half:
                    is_dsq = True

            if is_dsq:
                m = (d1 + 1) >> 1
            elif is_sq:
                m = (d1 - 1) >> 1
            else:
                m = d1 >> 1

            if m >= 3:
                term = m * (m - 1) * (m - 2) // 6
                local_total += term

        block_sums[b] = local_total

    return np.sum(block_sums)


def main():
    result = solve_biclinic(LIMIT_S)
    print(result)


if __name__ == "__main__":
    main()