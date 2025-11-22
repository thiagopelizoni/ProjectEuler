# Problem: https://projecteuler.net/problem=330
from tqdm import tqdm
from sympy.ntheory.modular import crt

def compute_ab(n: int, p: int):
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