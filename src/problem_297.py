# Problem: https://projecteuler.net/problem=297
import bisect
from functools import lru_cache

fib = [0, 1, 2]
while fib[-1] <= 2 * 10**17:
    next_f = fib[-1] + fib[-2]
    if next_f > 2 * 10**17:
        break
    fib.append(next_f)

@lru_cache(maxsize=None)
def sum_z(n: int) -> int:
    if n <= 0:
        return 0
    idx = bisect.bisect_right(fib, n) - 1
    f_k = fib[idx]
    sum_below = sum_z(f_k - 1)
    m_max = n - f_k
    num_using = m_max + 1
    sum_z_m = sum_z(m_max)
    sum_using = num_using + sum_z_m
    return sum_below + sum_using

def main():
    N = 10**17 - 1
    print(sum_z(N))

if __name__ == "__main__":
    main()