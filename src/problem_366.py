# Problem: https://projecteuler.net/problem=366
def main():
    """
    Purpose
    -------
    Solves Project Euler problem 366 by computing the sum of M(n) for n <= 10^18 modulo 10^8, where M(n) is the
    maximum number of stones the first player can take from a winning position or 0 otherwise.

    Method / Math Rationale
    -----------------------
    Identifies losing positions as a shifted Fibonacci sequence L_k with L_1=1, L_2=2, L_k = L_{k-1} + L_{k-2}.
    Defines intervals I_k between losing positions and sequences S_k of M(n) in each interval. Computes prefix
    lengths p_k using the recurrence p_k = p_{k-1} + p_{k-2} + (0 if k % 3 == 2 else 1) for k >= 5, with base
    values. Computes interval sums recursively using structural properties without constructing sequences,
    handling the final partial interval directly since it falls within the prefix.

    Complexity
    ----------
    O(log_phi N) time for generating Fibonacci numbers and computing sums, where phi is the golden ratio; O(1) space
    beyond lists of size O(log_phi N) ~ 90.

    References
    ----------
    https://projecteuler.net/problem=366
    """
    N = 10**18
    MOD = 10**8

    L = []
    a, b = 1, 2

    while a <= N:
        L.append(a)
        a, b = b, a + b

    num_intervals = len(L)
    p = [0] * (num_intervals + 1)
    l = [0] * (num_intervals + 1)
    sum_s = [0] * (num_intervals + 1)
    p[3] = 1
    p[4] = 2

    for k in range(3, num_intervals + 1):
        l[k] = L[k - 2] - 1

    for k in range(5, num_intervals + 1):
        d = 0 if k % 3 == 2 else 1
        p[k] = p[k - 1] + p[k - 2] + d

    for k in range(3, num_intervals + 1):
        if k == 3 or k == 4:
            sum_s[3] = 1
            sum_s[4] = 1 + 2
            continue
        r = p[k] - l[k - 1] - 1
        sum_prefix = p[k] * (p[k] + 1) // 2
        sum_r = r * (r + 1) // 2
        sum_s[k] = sum_prefix + sum_s[k - 2] - sum_r

    total = 0

    for k in range(3, num_intervals):
        total += sum_s[k]

    # Last interval
    last_l = L[-1]
    num = N - last_l

    # Since num < p[num_intervals], sum 1 to num
    partial = num * (num + 1) // 2

    total += partial
    print(total % MOD)

if __name__ == "__main__":
    main()