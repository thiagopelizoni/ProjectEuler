# Problem: https://projecteuler.net/problem=444
from decimal import Decimal, getcontext
from math import factorial

getcontext().prec = 50

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 444 by computing S_{20}(10^{14}) where S_k(N) is defined recursively with E(p)
    as the p-th harmonic number H_p, and outputs the result in scientific notation rounded to 10 significant digits.

    Method / Math Rationale
    -------------------------
    E(p) = H_p, the p-th harmonic number.
    S_1(N) = sum_{p=1}^N H_p.
    S_k(N) = sum_{p=1}^N S_{k-1}(p) for k > 1.
    The closed form is S_k(N) = binom(N + k, k) * (H_{N + k} - H_k).
    Compute binom(N + 20, 20) using product formula in high precision Decimal.
    Approximate H_{N + 20} using ln(N + 20) + Euler's constant + 1/(2*(N + 20)) - 1/(12*(N + 20)^2).
    Compute H_20 exactly as sum of reciprocals.
    Multiply and format the result.

    Complexity
    ----------
    O(1) time and space, as computations are fixed-size with high precision arithmetic.

    References
    ----------
    https://projecteuler.net/problem=444
    """
    N = 10**14
    m = 20
    n = Decimal(N + m)
    binom_val = Decimal(1)
    for i in range(1, m + 1):
        binom_val *= (n - Decimal(i - 1)) / Decimal(i)

    gamma = Decimal('0.57721566490153286060651209008240243104215933593992')
    ln_n = n.ln()
    one_over_2n = Decimal(1) / (Decimal(2) * n)
    one_over_12n2 = Decimal(1) / (Decimal(12) * n * n)
    H_large = ln_n + gamma + one_over_2n - one_over_12n2
    H_m = Decimal(0)
    for k in range(1, m + 1):
        H_m += Decimal(1) / Decimal(k)

    diff = H_large - H_m
    result = binom_val * diff
    s = f'{result:.9e}'
    print(s.replace('e+', 'e'))

if __name__ == "__main__":
    main()