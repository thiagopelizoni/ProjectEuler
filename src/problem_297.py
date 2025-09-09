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
    """
    Purpose
    Solve Project Euler problem 297: find the sum of z(n) for 1 <= n < 10^{17}, where z(n) is the number of terms
    in the Zeckendorf representation of n.

    Method / Math Rationale
    Uses a memoized recursive function to compute the sum. For a given n, find the largest Fibonacci f_k <= n.
    The sum up to n is the sum up to f_k - 1 plus the contributions from f_k to n, which is (m_max + 1) +
    sum_z(m_max), where m_max = n - f_k.
    The Fibonacci sequence is generated starting with 1 and 2 as per the problem.

    Complexity
    With memoization, the time complexity is O(L^2) in the worst case, where L ≈ 84 is the number of Fibonacci
    numbers up to 10^{17}, but in practice much faster.

    References
    https://projecteuler.net/problem=297
    """
    N = 10**17 - 1
    print(sum_z(N))

if __name__ == "__main__":
    main()