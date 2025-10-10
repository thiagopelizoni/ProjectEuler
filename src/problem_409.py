# Problem: https://projecteuler.net/problem=409
from tqdm import tqdm

def compute_inverses(max_val, mod):
    inv = [0] * (max_val + 1)
    inv[1] = 1

    for i in range(2, max_val + 1):
        inv[i] = (mod - (mod // i) * inv[mod % i]) % mod

    return inv

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 409 by computing W(10000000) mod 1000000007,
    where W(n) is the number of winning Nim positions with n distinct non-empty
    piles, each of size less than 2^n.

    Method / Math Rationale
    -----------------------
    Models pile sizes as non-zero vectors in GF(2)^n. Uses character sum to
    derive a closed-form involving a binomial coefficient reduced via Lucas'
    theorem, and computes large products and factorials modulo the prime
    1000000007.

    Complexity
    ----------
    O(n) time for loops computing inverses, binomial coefficients, falling
    factorials, and n!; O(n/2) space for inverse array.

    References
    ----------
    https://projecteuler.net/problem=409
    """
    n = 10000000
    MOD = 1000000007
    k = n // 2
    inv = compute_inverses(k, MOD)
    two_nm1 = pow(2, n - 1, MOD)
    r = (two_nm1 - 1) % MOD
    binom_val = 1
    for i in range(1, k + 1):
        num = (r - i + 1) % MOD
        binom_val = binom_val * num % MOD
        binom_val = binom_val * inv[i] % MOD

    c = (pow(-1, (n + 1) // 2, MOD) * binom_val) % MOD
    two_n = pow(2, n, MOD)
    m_mod = (two_n - 1) % MOD
    p = 1

    for j in tqdm(range(n)):
        term = (m_mod - j) % MOD
        p = p * term % MOD

    fact_n = 1
    for i in range(1, n + 1):
        fact_n = fact_n * i % MOD

    inside = (p - fact_n * c % MOD + MOD) % MOD
    two_n_m1 = (two_n - 1) % MOD
    inv_two_n = pow(two_n, MOD - 2, MOD)
    w = two_n_m1 * inside % MOD * inv_two_n % MOD
    print(w)

if __name__ == "__main__":
    main()