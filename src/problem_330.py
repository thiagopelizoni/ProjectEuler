# Problem: https://projecteuler.net/problem=330
from tqdm import tqdm
from sympy.ntheory.modular import crt

def compute_ab(n: int, p: int):
    """
    Purpose
    -------
    Computes A(n) mod p and B(n) mod p for the sequences in Project Euler 330.

    Args
    ----
    n: The index for A(n) and B(n).
    p: Prime modulus.

    Returns
    -------
    Tuple (A(n) % p, B(n) % p).

    Method / Math Rationale
    ------------------------
    Uses recurrences A(n) = n! + sum_{k=0}^{n-1} binom(n,k) A(k),
    B(n) = sum_{k=0}^{n-1} binom(n,k) B(k) - sum_{j=0}^n n!/j! for all n,
    where sum_{j=0}^n n!/j! = T(n) with T(0)=1, T(n)=1 + n T(n-1).
    For n >= p, n! ≡ 0 mod p. Binomial rows via Pascal's triangle mod p.
    Sequences periodic mod p with period p(p-1) from n=p.

    Complexity
    ----------
    O(p^4) time per prime due to O((p^2)^2) binomial and sum computations;
    negligible for p=137.

    References
    ----------
    https://projecteuler.net/problem=330
    """
    if p == 2:
        per = 2
    else:
        per = p * (p - 1)
    maxn = p + per
    fact = [1] * p
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    T = [0] * (maxn + 1)
    T[0] = 1
    for nn in range(1, maxn + 1):
        T[nn] = (1 + (nn % p) * T[nn - 1]) % p
    A = [0] * (maxn + 1)
    B = [0] * (maxn + 1)
    A[0] = 1 % p
    B[0] = p - 1
    binoms = [1]
    for nn in tqdm(range(1, maxn + 1), desc=f"Computing for p={p}"):
        new_binoms = [0] * (nn + 1)
        new_binoms[0] = 1
        for k in range(1, nn):
            new_binoms[k] = (binoms[k - 1] + binoms[k]) % p
        new_binoms[nn] = 1
        sA = 0
        sB = 0
        for k in range(nn):
            sA = (sA + new_binoms[k] * A[k]) % p
            sB = (sB + new_binoms[k] * B[k]) % p
        extraA = fact[nn] % p if nn < p else 0
        A[nn] = (sA + extraA) % p
        extraB = T[nn]
        B[nn] = (sB - extraB + p) % p
        binoms = new_binoms
    if n == 0:
        return A[0], B[0]
    if n < p:
        return A[n], B[n]
    offset = (n - p) % per
    return A[p + offset], B[p + offset]

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 330: Compute A(10^9) + B(10^9) mod 77777777.

    Method / Math Rationale
    ------------------------
    Factor 77777777 = 7*11*73*101*137. For each prime p, compute
    (A(10^9) + B(10^9)) mod p using periodic recurrences mod p
    with binomial transform and T(n) for B's inhomogeneity.
    Combine via Chinese Remainder Theorem.

    Complexity
    ----------
    O(sum_p p^4) ~ O(10^9) operations total, acceptable.

    References
    ----------
    https://projecteuler.net/problem=330
    """
    primes = [7, 11, 73, 101, 137]
    n = 10**9
    remainders = []
    for p in primes:
        a, b = compute_ab(n, p)
        remainders.append((a + b) % p)
    ans = crt(primes, remainders)[0]
    print(ans)

if __name__ == "__main__":
    main()