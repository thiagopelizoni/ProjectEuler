# Problem: https://projecteuler.net/problem=401
from tqdm import tqdm
import math


def sum_of_squares(n, mod):
    if n < 0:
        return 0
    a = n
    b = n + 1
    c = 2 * n + 1
    if a % 2 == 0:
        a //= 2
    else:
        b //= 2
    if a % 3 == 0:
        a //= 3
    elif b % 3 == 0:
        b //= 3
    else:
        c //= 3
    return (a % mod * (b % mod) * (c % mod)) % mod


def main():
    """
    Purpose
    -------
    Computes SIGMA2(10^15) modulo 10^9, where SIGMA2(n) is the summatory function
    of the sum of squares of divisors, i.e., sum_{i=1}^n sum_{d|i} d^2.

    Method / Math Rationale
    -----------------------
    SIGMA2(n) = sum_{d=1}^n d^2 * floor(n/d). This is computed efficiently by
    grouping terms with the same floor(n/d) value using an O(sqrt(n)) loop over
    segments [i, j-1]. For each segment, compute floor(n/d) * (sum_{k=1}^{j-1} k^2
    - sum_{k=1}^{i-1} k^2) modulo 10^9, where sum of squares uses a closed-form
    formula adjusted for modular arithmetic by pre-dividing factors to avoid large
    intermediates.

    Complexity
    ----------
    Time: O(sqrt(n)) ~ 3*10^7 operations for n=10^15
    Space: O(1)

    References
    ----------
    https://projecteuler.net/problem=401
    """
    LIMIT = 10**15
    MOD = 10**9
    ans = 0
    i = 1
    approx_iters = int(2 * math.sqrt(LIMIT))
    with tqdm(total=approx_iters) as pbar:
        while i <= LIMIT:
            q = LIMIT // i
            j = LIMIT // q + 1
            cursum = (sum_of_squares(j - 1, MOD) - sum_of_squares(i - 1, MOD) + MOD) % MOD
            ans = (ans + q * cursum % MOD) % MOD
            i = j
            pbar.update(1)
    print(ans)


if __name__ == "__main__":
    main()