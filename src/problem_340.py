# Problem: https://projecteuler.net/problem=340
def main():
    """
    Purpose
    -------
    Solves Project Euler problem 340 by computing the last 9 digits of S(a, b, c) where a=21^7, b=7^21, c=12^7.

    Method / Math Rationale
    ------------------------
    For each n from 0 to b, F(n) = 4 * (d + 1) * a + n - (3 * d + 4) * c where d = floor((b - n) / a).
    Group the n by their d = k, each group is a consecutive range. Use closed-form formulas to sum over the full groups
    (k=0 to m-1 where m = floor(b / a)) and the partial group (k=m).

    Complexity
    ----------
    O(1) time and space.

    References
    ----------
    https://projecteuler.net/problem=340
    """
    A = 21 ** 7
    B = 7 ** 21
    C = 12 ** 7
    MOD = 1000000000

    m = B // A
    r = B % A
    p = m - 1 if m > 0 else 0

    # Constant part for full groups k=0 to p
    sum_k_plus_1 = (p + 1) * (p + 2) // 2
    sum_3k_plus_4 = (p + 1) * (3 * p + 8) // 2
    const_full = 4 * A * A * sum_k_plus_1 - A * C * sum_3k_plus_4

    # Sum of n over full groups
    sum_low_high = (p + 1) * (2 * B + 1 - A) - A * p * (p + 1)
    sum_n_full = (A * sum_low_high) // 2

    full_sum = const_full + sum_n_full

    # Partial group k=m, n=0 to r
    num_partial = r + 1
    const_partial = 4 * (m + 1) * A - (3 * m + 4) * C
    sum_n_partial = r * (r + 1) // 2
    partial_sum = num_partial * const_partial + sum_n_partial

    S = full_sum + partial_sum
    print(S % MOD)

if __name__ == "__main__":
    main()