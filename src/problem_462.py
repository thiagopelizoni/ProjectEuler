# Problem: https://projecteuler.net/problem=462
from decimal import Decimal, getcontext
from math import floor

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 462: computes F(10^18), the number of permutations of 3-smooth numbers <= 10^18 where each number appears after all its
    proper divisors in the permutation.

    Method / Math Rationale
    -----------------------
    The set S(N) consists of numbers 2^a * 3^b <= N. The poset under divisibility is isomorphic to the Young diagram poset with partition lambda where
    lambda[a] = 1 + max b for each a (exponent of 2).
    F(N) is the number of standard Young tableaux of this shape, computed via the hook-length formula: n! / product of hook lengths over all boxes,
    where n = |S(N)|.
    We compute log10 of this value for precision, then derive the mantissa and exponent for scientific notation.

    Complexity
    ----------
    O((log N)^2) time to compute the partition, conjugate, and sum logarithms over O((log N)^2) boxes.

    References
    ----------
    https://projecteuler.net/problem=462
    """
    N = 10**18
    max_a = 0
    while (1 << max_a) <= N:
        max_a += 1

    max_a -= 1
    lambda_part = []
    for a in range(max_a + 1):
        current = 1 << a
        M = N // current
        p = 1
        k = 0
        while p * 3 <= M:
            p *= 3
            k += 1
        lambda_part.append(k + 1)

    n = sum(lambda_part)
    max_col = lambda_part[0]
    conj = []
    for j in range(1, max_col + 1):
        count = 0
        for lam in lambda_part:
            if lam >= j:
                count += 1
            else:
                break
        conj.append(count)

    getcontext().prec = 30
    log10_f = Decimal(0)
    for k in range(2, n + 1):
        log10_f += Decimal(k).log10()

    l = len(lambda_part)
    for row in range(1, l + 1):
        lam_r = lambda_part[row - 1]
        for col in range(1, lam_r + 1):
            hook = lam_r - col + conj[col - 1] - row + 1
            log10_f -= Decimal(hook).log10()

    exp = floor(log10_f)
    frac = log10_f - Decimal(exp)
    mant = Decimal(10) ** frac
    result = f"{mant:.10f}e{exp}"
    print(result)

if __name__ == "__main__":
    main()