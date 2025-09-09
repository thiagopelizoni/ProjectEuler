# Problem: https://projecteuler.net/problem=294
from mpmath import mp, mpc, mpf, exp, pi, floor, nint

mp.dps = 400

def mul_trunc(p1, p2, deg=24):
    res = [mpc(0) for _ in range(deg)]
    len1 = len(p1)
    len2 = len(p2)
    for i in range(len1):
        for j in range(len2):
            if i + j >= deg:
                break
            res[i + j] += p1[i] * p2[j]
    return res

def poly_pow(base, exponent, deg=24):
    result = [mpc(1)] + [mpc(0)] * (deg - 1)
    while exponent > 0:
        if exponent % 2 == 1:
            result = mul_trunc(result, base)
        base = mul_trunc(base, base)
        exponent //= 2
    return result

def main():
    """
    Purpose
    Computes S(11**12) modulo 10**9, where S(n) is the number of positive integers k < 10**n with digit sum 23 and divisible by 23.

    Args
    None

    Returns
    None

    Method / Math Rationale
    Uses roots of unity filter to enforce the modulo 23 constraint. Groups positions into cycles of 22 due to the multiplicative order of 10 modulo 23. Computes truncated polynomial powers and products using high-precision complex numbers to extract the required coefficient, averages over roots, rounds to integer, and takes modulo 10**9.

    Complexity
    O(23 * log(M) * D**2) with D=24 and M approx 10**12, resulting in constant time in practice.

    References
    https://projecteuler.net/problem=294
    """
    n = 11 ** 12
    period = 22
    m = n // period
    r = n % period
    modulus = 23
    target_sum = 23
    deg = target_sum + 1
    mod_out = mpf(1000000000)
    powers = [0] * period
    powers[0] = 1
    for i in range(1, period):
        powers[i] = (powers[i - 1] * 10) % modulus
    zeta = exp(2 * pi * mpc(0, 1) / modulus)
    total = mpc(0)
    for k in range(modulus):
        eta = zeta ** k
        cycle_poly = [mpc(1)]
        for j in range(period):
            c = eta ** powers[j]
            pos_poly = []
            cp = mpc(1)
            for d in range(10):
                pos_poly.append(cp)
                cp *= c
            cycle_poly = mul_trunc(cycle_poly, pos_poly, deg)
        cycle_pow = poly_pow(cycle_poly, m, deg)
        remain_poly = [mpc(1)]
        for j in range(r):
            c = eta ** powers[j]
            pos_poly = []
            cp = mpc(1)
            for d in range(10):
                pos_poly.append(cp)
                cp *= c
            remain_poly = mul_trunc(remain_poly, pos_poly, deg)
        full_poly = mul_trunc(cycle_pow, remain_poly, deg)
        total += full_poly[target_sum]
    total /= modulus
    real_part = total.real
    q = floor(real_part / mod_out)
    remainder = real_part - q * mod_out
    answer = int(nint(remainder))
    print(answer)

if __name__ == "__main__":
    main()
