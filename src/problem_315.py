import numpy as np
from numba import njit, prange

# 0: abcdef  (0x3F)
# 1: bc      (0x06)
# 2: abdeg   (0x5B)
# 3: abcdg   (0x4F)
# 4: bcfg    (0x66)
# 5: acdfg   (0x6D)
# 6: acdefg  (0x7D)
# 7: abcf    (0x27)
# 8: abcdefg (0x7F)
# 9: abcdfg  (0x6F)
MASKS = np.array([0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x27, 0x7F, 0x6F], dtype=np.int32)

@njit(fastmath=True, cache=True)
def get_primes(n):
    size = n // 2
    sieve = np.ones(size, dtype=np.bool_)
    limit = int(n**0.5)
    for i in range(1, (limit - 1) // 2 + 1):
        if sieve[i]:
            val = 2 * i + 1
            start_idx = (val * val) // 2
            sieve[start_idx::val] = False
    count = 1 + np.sum(sieve[1:])
    primes = np.empty(count, dtype=np.int32)
    primes[0] = 2
    write_idx = 1
    for i in range(1, size):
        if sieve[i]:
            primes[write_idx] = 2 * i + 1
            write_idx += 1
    return primes


@njit(fastmath=True, cache=True)
def count_set_bits(n):
    c = 0
    while n > 0:
        n &= n - 1
        c += 1
    return c


@njit(fastmath=True, cache=True)
def calc_saved_segments(current, next_val):
    saved = 0
    while current > 0 or next_val > 0:
        d1 = current % 10
        d2 = next_val % 10
        m1 = 0
        if current > 0:
            m1 = MASKS[d1]
        m2 = 0
        if next_val > 0:
            m2 = MASKS[d2]
        common = m1 & m2
        if common > 0:
            saved += 2 * count_set_bits(common)
        current //= 10
        next_val //= 10
    return saved


@njit(parallel=True, fastmath=True, cache=True)
def solve_p315(lower_bound, upper_bound):
    primes = get_primes(upper_bound)
    start_idx = 0
    len_p = len(primes)
    while start_idx < len_p and primes[start_idx] < lower_bound:
        start_idx += 1
    total_diff = 0
    for i in prange(start_idx, len_p):
        p = primes[i]
        current_saved = 0
        curr = p
        while curr >= 10:
            temp = curr
            next_val = 0
            while temp > 0:
                next_val += temp % 10
                temp //= 10
            current_saved += calc_saved_segments(curr, next_val)
            curr = next_val
        total_diff += current_saved
    return total_diff


def main():
    LOWER = 10_000_000
    UPPER = 20_000_000
    solve_p315(100, 200)
    result = solve_p315(LOWER, UPPER)
    print(result)


if __name__ == "__main__":
    main()