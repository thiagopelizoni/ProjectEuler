# Problem: https://projecteuler.net/problem=474
from math import gcd
import numpy as np
from tqdm import tqdm
import numba
from sympy.ntheory import primerange

@numba.jit(nopython=True)
def my_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

@numba.jit(nopython=True)
def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

@numba.jit(nopython=True)
def compute_order(p, m):
    if my_gcd(p, m) != 1:
        return 0
    o = 5000
    for f in (2, 5):
        while o % f == 0:
            if mod_pow(p, o // f, m) == 1:
                o //= f
            else:
                break
    return o

@numba.jit(nopython=True)
def compute_exponent(p, n):
    e = 0
    temp = n
    while temp > 0:
        temp //= p
        e += temp
    return e

@numba.jit(nopython=True)
def update_dp(dp, p, e, m, P, units):
    p_m = p % m
    d = compute_order(p_m, m)
    if d == 0:
        return dp
    q = (e + 1) // d
    r = (e + 1) % d
    G = np.zeros(d, dtype=np.int64)
    power = np.int64(1)
    for i in range(d):
        G[i] = power
        power = (power * p_m) % m
    new_dp = np.zeros(m, dtype=np.int64)
    num_units = len(units)
    for pos in range(d):
        multi = np.int64(q + (1 if pos < r else 0))
        if multi == 0:
            continue
        g = G[pos]
        for k in range(num_units):
            i = units[k]
            new_i = (i * g) % m
            new_dp[new_i] = (new_dp[new_i] + multi * dp[i]) % P
    return new_dp

def chinese_remainder(a1, a2, m1, m2):
    inv = pow(m1, -1, m2)
    c = a1 + m1 * ((a2 - a1) * inv % m2)
    return c % (m1 * m2)

def main():
    """
    Purpose
    -------
    Computes F(10^6!, 65432) mod (10^16 + 61), where F(n, d) is the number of divisors of n whose last
    digits equal the digits of d (here 5 digits).

    Method / Math Rationale
    ------------------------
    Divisors d of n = 10^6! with d ≡ 65432 mod 10^5 must have v2(d) = 3, v5(d) = 0.
    Let c = d / 8, then c divides the 10-coprime part N' of n!, and c ≡ s mod 12500 for computed s.
    Use DP to count divisors of N' congruent to residues mod 12500, updating for each prime by shifting
    residues using powers, grouping for efficiency with cycles.

    Complexity
    ----------
    O(π(10^6) * avg(order) * φ(12500)) ≈ 7.8e4 * 1500 * 5000 ≈ 6e11 operations; uses numba for acceleration.

    References
    ----------
    https://projecteuler.net/problem=474
    """
    n = 1000000
    M = 100000
    r = 65432
    m = 12500
    P = 10**16 + 61

    m2 = 4
    m5 = 3125
    r5 = r % m5
    inv8 = pow(8, -1, m5)
    s2 = (r5 * inv8) % m5
    s1 = 3
    s = chinese_remainder(s1, s2, m2, m5)

    dp = np.zeros(m, dtype=np.int64)
    dp[1] = 1

    primes = list(primerange(3, n + 1))
    units_list = [i for i in range(m) if gcd(i, m) == 1]
    units = np.array(units_list, dtype=np.int64)

    for prime in tqdm(primes):
        if prime == 5:
            continue
        e = compute_exponent(prime, n)
        dp = update_dp(dp, prime, e, m, P, units)

    print(dp[s])

if __name__ == "__main__":
    main()