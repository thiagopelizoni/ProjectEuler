# Problem: https://projecteuler.net/problem=388
from functools import lru_cache
from tqdm import tqdm
import math

def linear_mobius_sieve(limit):
    mu = [0] * (limit + 1)
    is_prime = [True] * (limit + 1)
    primes = []
    mu[1] = 1
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    M = [0] * (limit + 1)
    for i in range(1, limit + 1):
        M[i] = M[i - 1] + mu[i]
    return mu, M

PRELIMIT = 1000000
_, preM = linear_mobius_sieve(PRELIMIT)

@lru_cache(maxsize=None)
def M(x):
    if x < 0:
        return 0
    if x <= PRELIMIT:
        return preM[x]
    s = 0
    l = 2
    while l <= x:
        k = x // l
        r = min(x, x // k)
        s += (r - l + 1) * M(k)
        l = r + 1
    return 1 - s

def main():
    N = 10**10
    s = 0
    l = 1
    pbar = tqdm(total=math.isqrt(N) * 2)
    while l <= N:
        k = N // l
        r = min(N, N // k)
        m = k + 1
        s += (M(r) - M(l - 1)) * (m**3 - 1)
        pbar.update(r - l + 1)
        l = r + 1
    pbar.close()
    d_str = str(s)
    print(d_str[:9] + d_str[-9:])

if __name__ == "__main__":
    main()