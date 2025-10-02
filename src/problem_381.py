# Problem: https://projecteuler.net/problem=381
from tqdm import tqdm

def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 381: compute the sum of S(p) for all primes
    5 <= p < 10^8, where S(p) = sum_{k=1}^5 (p-k)! mod p.

    Method / Math Rationale
    ------------------------
    Using Wilson's Theorem: (p-1)! ≡ -1 mod p.
    Then (p-k)! ≡ (-1)^k * (k-1)!^{-1} mod p for k=1 to 5.
    Thus S(p) ≡ -inv(2) + inv(6) - inv(24) mod p.
    Compute inv(3,p) using extended Euclidean algorithm, inv(2,p) = (p+1)//2,
    then derive inv(6) and inv(24).
    Primes generated via Sieve of Eratosthenes.

    Complexity
    ----------
    Time: O(N log log N) for sieve + O(pi(N) * log N) for inverses,
    where N=10^8.
    Space: O(N)

    References
    ----------
    https://projecteuler.net/problem=381
    """
    N = 100000000
    is_prime = [True] * N
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, N, i):
                is_prime[j] = False
    primes = [p for p in range(5, N) if is_prime[p]]
    total = 0
    for p in tqdm(primes):
        inv2 = (p + 1) // 2
        inv3 = mod_inverse(3, p)
        inv6 = (inv2 * inv3) % p
        inv2_sq = (inv2 * inv2) % p
        inv8 = (inv2_sq * inv2) % p
        inv24 = (inv8 * inv3) % p
        s = (-inv2 + inv6 - inv24) % p
        total += s
    print(total)

if __name__ == "__main__":
    main()