# Problem: https://projecteuler.net/problem=509
def main():
    """
    Purpose
    -------
    Solves Project Euler problem 509: computes S(123456787654321) modulo 1234567890 and prints the result.
    No parameters. No return value.

    Method / Math Rationale
    -----------------------
    The Grundy number g(x) is 0 if x is odd, otherwise the 2-adic valuation of x (exponent of 2 in its factorization).
    Count the numbers from 1 to n grouped by their Grundy value k.
    Losing positions are triples where g(a) XOR g(b) XOR g(c) = 0.
    Compute the sum of products of counts for such k values, modulo the given modulus.
    S(n) is n^3 minus this sum, modulo the modulus.

    Complexity
    ----------
    O((log n)^3) time due to triple loop over up to log2(n) ~ 50 values.
    O(log n) space for counts.

    References
    ----------
    https://projecteuler.net/problem=509
    """
    n = 123456787654321
    mod = 1234567890
    counts = [0] * 64
    counts[0] = (n + 1) // 2
    k = 1
    power = 2
    while True:
        div = n // power
        if div == 0:
            break
        counts[k] = (div + 1) // 2
        k += 1
        power *= 2
        if k >= 64:
            break
    max_k = k - 1
    losing = 0
    for i in range(max_k + 1):
        ci = counts[i] % mod
        for j in range(max_k + 1):
            cj = counts[j] % mod
            for l in range(max_k + 1):
                if (i ^ j ^ l) == 0:
                    cl = counts[l] % mod
                    add = (ci * cj % mod) * cl % mod
                    losing = (losing + add) % mod
    total = pow(n, 3, mod)
    result = (total - losing + mod) % mod
    print(result)

if __name__ == "__main__":
    main()