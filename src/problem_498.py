# Problem: https://projecteuler.net/problem=498
def comb_mod(a, b, mod):
    if b < 0 or b > a:
        return 0
    if b > a - b:
        b = a - b
    res = 1
    for i in range(b):
        res = (res * (a - i)) % mod
        res = (res * pow(i + 1, mod - 2, mod)) % mod
    return res

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 498 by computing C(10^13, 10^12, 10^4) mod 999999937, where C(n, m, d)
    is the absolute value of the coefficient of x^d in the remainder of x^n divided by (x-1)^m.

    Method / Math Rationale
    -----------------------
    The value is binom(n, d) * binom(n - d - 1, m - d - 1) mod 999999937.
    The first binomial is computed directly using iterative multiplication and modular inverses since d is small.
    The second uses Lucas' theorem since the arguments are large, decomposing into base-mod digits and
    computing smaller binomials.

    Complexity
    ----------
    O(d)

    References
    ----------
    https://projecteuler.net/problem=498
    """
    n = 10**13
    m = 10**12
    d = 10**4
    mod = 999999937
    first = comb_mod(n, d, mod)
    q = n - d - 1
    r = m - d - 1
    q1 = q // mod
    q0 = q % mod
    r1 = r // mod
    r0 = r % mod
    second = (comb_mod(q1, r1, mod) * comb_mod(q0, r0, mod)) % mod
    result = (first * second) % mod
    print(result)

if __name__ == "__main__":
    main()