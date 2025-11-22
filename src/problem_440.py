# Problem: https://projecteuler.net/problem=440
from math import gcd
from collections import defaultdict
from tqdm import tqdm
from sympy.functions.combinatorial.numbers import legendre_symbol
from sympy.ntheory import sqrt_mod

def main():

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