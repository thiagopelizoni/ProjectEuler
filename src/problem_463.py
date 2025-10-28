# Problem: https://projecteuler.net/problem=463
from functools import lru_cache

MOD = 1000000000

@lru_cache(maxsize=None)
def f(n: int) -> int:
    if n < 1:
        return 0
    if n == 1:
        return 1
    if n == 3:
        return 3
    if n % 2 == 0:
        return f(n // 2)
    elif n % 4 == 3:
        res = 3 * f((n - 1) // 2) - 2 * f((n - 3) // 4)
    else:
        res = 2 * f((n + 1) // 2) - f((n - 1) // 4)
    return (res % MOD + MOD) % MOD

@lru_cache(maxsize=None)
def S(n: int) -> int:
    if n < 1:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 5
    r = n % 4
    if r == 3:
        res = 6 * S((n - 1) // 2) - 8 * S((n - 3) // 4) - 1
    elif r == 2:
        res = S(n - 1) + f(n // 2)
    elif r == 1:
        res = S(n - 2) + f(n) + f((n - 1) // 2)
    else:
        res = S(n - 1) + f(n // 4)
    return (res % MOD + MOD) % MOD

def main():
    """
    Purpose
    -------
    Computes the last 9 digits of S(3**37), where S(n) is the sum from i=1 to n of f(i),
    and f is a function defined by a weird recurrence relation.

    Method / Math Rationale
    -----------------------
    Implements recursive functions for f and S with memoization using lru_cache.
    The function f follows the given recurrence. For S, uses a derived recurrence
    S(4n+3) = 6 * S(2n+1) - 8 * S(n) - 1, and incremental additions for other
    modulo 4 cases. All computations are performed modulo 10**9 to get the last
    9 digits.

    Complexity
    ----------
    O(log n) time and space, as the memoized recursion has logarithmic depth and
    a small number of unique calls.

    References
    ----------
    https://projecteuler.net/problem=463
    """
    n = 3 ** 37
    print(S(n))

if __name__ == "__main__":
    main()
