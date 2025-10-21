# Problem: https://projecteuler.net/problem=440
from math import gcd
from collections import defaultdict
from tqdm import tqdm
from sympy.functions.combinatorial.numbers import legendre_symbol
from sympy.ntheory import sqrt_mod

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 440 by computing S(2000) modulo 987898789, where S(L) is the triple sum
    over 1 <= a, b, c <= L of gcd(T(c^a), T(c^b)), and T(n) is the number of ways to tile a 1xn board
    using 1x1 tiles with digits or 1x2 blocks.

    Method / Math Rationale
    -----------------------
    Utilizes the property that gcd(T(m), T(n)) = U_gcd(m+1, n+1), where U is the related Lucas sequence
    with closed form (alpha^k - beta^k) / delta, alpha = 5 + sqrt(26), beta = 5 - sqrt(26), delta = alpha - beta.
    Groups exponent pairs (a, b) by whether v_2(a) equals v_2(b).
    For unequal valuations, gcd equals 10 if c is odd (corresponding to U_2), 1 if c is even (U_1).
    For equal v_2(a) = v_2(b) = i, expresses a = 2^i * x, b = 2^i * y with x, y odd, then the effective
    exponent for U is c^(2^i * gcd(x, y)) + 1, computed modulo M using Binet form with exponents reduced
    modulo phi(M) = M - 1 via modular exponentiation.

    Complexity
    ----------
    Precomputation: O(L^2) time for computing gcd distributions across all i.
    Main computation: O(L * sum_{i=0}^{10} (L / 2^{i+1})^2 * log M) due to the loop over c, i, and pairs
    implicitly via mult, with pow operations; with L=2000, highly efficient.

    References
    ----------
    https://projecteuler.net/problem=440
    """

    M = 987898789
    L = 2000
    phi = M - 1

    count = []
    for i in range(12):
        count.append(L // (1 << i) - L // (1 << (i + 1)))

    sum_sq = sum(c * c for c in count)
    num_unequal = L * L - sum_sq

    num_even = L // 2
    num_odd = L - num_even

    sum_u = num_odd * 10 + num_even * 1

    unequal_contrib = (sum_u * num_unequal) % M

    max_i = 11
    mults = []
    for i in range(max_i):
        m_i = L // (1 << i)
        o_i = list(range(1, m_i + 1, 2))
        mult = defaultdict(int)
        for x in o_i:
            for y in o_i:
                mult[gcd(x, y)] += 1
        mults.append(mult)

    if legendre_symbol(26, M) != 1:
        raise ValueError("26 is not a quadratic residue modulo M")

    s = sqrt_mod(26, M)

    alpha = (5 + s) % M
    beta = (5 - s) % M

    delta = (alpha - beta) % M

    inv_delta = pow(delta, M - 2, M)

    total_s = unequal_contrib

    for c in tqdm(range(1, L + 1)):
        for ii in range(max_i):
            mult = mults[ii]
            contrib = 0
            for d, cnt in mult.items():
                exponent = (1 << ii) * d
                base_pow = pow(c, exponent, phi)
                r_mod = (base_pow + 1) % phi
                ap = pow(alpha, r_mod, M)
                bp = pow(beta, r_mod, M)
                diff = (ap - bp + M) % M
                u = (diff * inv_delta) % M
                contrib = (contrib + cnt * u) % M
            total_s = (total_s + contrib) % M

    print(total_s)

if __name__ == "__main__":
    main()