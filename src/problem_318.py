import math
from numba import njit, prange

TARGET = 2011

@njit(parallel=True, fastmath=True, cache=True)
def solve(limit):
    total_n = 0
    p_max = limit // 2
    for p in prange(1, p_max + 1):
        sqrt_p = math.sqrt(p)
        q_limit_sum = limit - p
        for q in range(p + 1, q_limit_sum + 1):
            sqrt_q = math.sqrt(q)
            diff = sqrt_q - sqrt_p
            if diff >= 1.0:
                break
            denom = -2.0 * math.log10(diff)
            n = math.ceil(limit / denom)
            total_n += int(n)
    return total_n

def main():
    result = solve(TARGET)
    print(result)

if __name__ == "__main__":
    main()
