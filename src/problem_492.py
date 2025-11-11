# Problem: https://projecteuler.net/problem=492

import math
from tqdm import tqdm


def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]


def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def sqrt_mod(a, p):
    if legendre_symbol(a, p) != 1:
        raise ValueError("No square root")
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    if p == 2:
        return a % 2
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    m = e
    c = pow(n, s, p)
    t = pow(a, s, p)
    r = pow(a, (s + 1) // 2, p)
    while t != 1:
        t2 = t
        i = 0
        while t2 != 1:
            t2 = pow(t2, 2, p)
            i += 1
            if i == m:
                raise ValueError("Error in Tonelli-Shanks")
        b = pow(c, pow(2, m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


class FieldElement:
    def __init__(self, a, b, p):
        self.a = a % p
        self.b = b % p
        self.p = p

    def __add__(self, other):
        return FieldElement(self.a + other.a, self.b + other.b, self.p)

    def __mul__(self, other):
        aa = (self.a * other.a + self.b * other.b * 13) % self.p
        bb = (self.a * other.b + self.b * other.a) % self.p
        return FieldElement(aa, bb, self.p)

    def pow(self, exp):
        res = FieldElement(1, 0, self.p)
        base = self
        while exp > 0:
            if exp % 2 == 1:
                res = res * base
            base = base * base
            exp //= 2
        return res


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 492 by computing B(10^9, 10^7, 10^15), which is the sum of a_{10^15} mod p over all primes p in [10^9, 10^9 + 10^7].
    No parameters. Prints the result.

    Method / Math Rationale
    -----------------------
    The sequence a_n satisfies a_{n+1} = 6 a_n^2 + 10 a_n + 3 with a_1 = 1.
    Transform to b_n = 6 a_n + 5, yielding b_{n+1} = b_n^2 - 2 with b_1 = 11.
    Then b_n = u_{2^{n-1}} where u_k satisfies u_k = 11 u_{k-1} - u_{k-2} with u_0 = 2, u_1 = 11.
    Compute u_k mod p using closed form u_k = alpha^k + beta^k mod p, where alpha, beta = [11 ± 3 sqrt(13)] / 2.
    If 13 is quadratic residue mod p, compute in F_p; else in F_{p^2}.
    Reduce exponent 2^{n-1} mod phi(field) to make computation feasible.

    Complexity
    ----------
    Time: O(π(10^7) * log(10^{18})) ≈ 5*10^5 * 120 = 6*10^7 operations, efficient.
    Space: O(1) per prime.

    References
    ----------
    https://projecteuler.net/problem=492
    """
    x = 10**9
    y = 10**7
    nn = 10**15
    mm = nn - 1
    low = x
    high = x + y

    small_limit = int(math.sqrt(high)) + 1
    small_primes = sieve(small_limit)

    is_prime_seg = [True] * (high - low + 1)
    for p in small_primes:
        if p * p > high:
            break
        start = max(p * p, ((low + p - 1) // p) * p)
        for j in range(start, high + 1, p):
            if j != p:
                is_prime_seg[j - low] = False

    primes = [low + i for i in range(high - low + 1) if is_prime_seg[i]]

    total = 0
    for p in tqdm(primes):
        ls = legendre_symbol(13, p)
        inv2 = (p + 1) // 2
        inv6 = pow(6, p - 2, p)
        if ls == 1:
            s = sqrt_mod(13, p)
            alpha = (11 + 3 * s) * inv2 % p
            beta = (11 + p - 3 * s) * inv2 % p
            phi = p - 1
            ee = pow(2, mm, phi)
            alpha_pow = pow(alpha, ee, p)
            beta_pow = pow(beta, ee, p)
            uu = (alpha_pow + beta_pow) % p
        else:
            phi = p * p - 1
            ee = pow(2, mm, phi)
            a_part = 11 * inv2 % p
            b_part = 3 * inv2 % p
            alpha = FieldElement(a_part, b_part, p)
            alpha_pow = alpha.pow(ee)
            uu = (2 * alpha_pow.a) % p
        a_mod = ((uu - 5) % p) * inv6 % p
        total += a_mod

    print(total)


if __name__ == "__main__":
    main()