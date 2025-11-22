# Problem: https://projecteuler.net/problem=432
import sys
from functools import lru_cache
from tqdm import tqdm

def main():
    sys.setrecursionlimit(10000)
    N = 510510
    M = 10**11
    MOD = 10**9
    L = 10**7
    phi = list(range(L + 1))
    for i in tqdm(range(2, L + 1)):
        if phi[i] == i:
            for j in range(i, L + 1, i):
                phi[j] = phi[j] // i * (i - 1)
    sum_small = [0] * (L + 1)
    for i in range(1, L + 1):
        sum_small[i] = sum_small[i - 1] + phi[i]

    @lru_cache(None)
    def sum_phi(x: int) -> int:
        if x == 0:
            return 0
        if x <= L:
            return sum_small[x]
        res = x * (x + 1) // 2
        l = 2
        while l <= x:
            q = x // l
            r = x // q
            res -= (r - l + 1) * sum_phi(q)
            l = r + 1
        return res

    primes = [2, 3, 5, 7, 11, 13, 17]

    @lru_cache(None)
    def S(n: int, m: int) -> int:
        if m == 0:
            return 0
        if n == 1:
            return sum_phi(m)
        p = None
        q = None
        for pp in primes:
            if n % pp == 0:
                p = pp
                q = n // p
                break
        res = 0
        pow_p = 1
        while True:
            ka = m // pow_p
            if ka == 0:
                break
            res += pow_p * (p - 1) * (S(q, ka) - S(n, ka // p))
            pow_p *= p
        return res

    ans = S(N, M)
    print(ans % MOD)

if __name__ == "__main__":
    main()