# Problem: https://projecteuler.net/problem=340
def main():
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