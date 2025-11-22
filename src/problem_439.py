# Problem: https://projecteuler.net/problem=439
from functools import lru_cache
from math import isqrt
from tqdm import tqdm

def main():
    MOD = 10**9
    N = 10**11
    LIMIT = 10**6

    mu = [0] * (LIMIT + 1)
    mu[1] = 1
    vis = [False] * (LIMIT + 1)
    primes = []
    for i in range(2, LIMIT + 1):
        if not vis[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > LIMIT:
                break
            vis[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    pre_P = [0] * (LIMIT + 1)
    for i in range(1, LIMIT + 1):
        pre_P[i] = pre_P[i - 1] + mu[i] * i

    memo_P = {}

    def get_P(m):
        if m < 0:
            return 0
        if m <= LIMIT:
            return pre_P[m]
        if m in memo_P:
            return memo_P[m]
        sq = isqrt(m)
        sum1 = 0
        for d in range(2, sq + 1):
            sum1 += d * get_P(m // d)
        sum2 = 0
        for kk in range(1, sq + 1):
            left = max(sq + 1, m // (kk + 1) + 1)
            right = m // kk
            if left > right:
                continue
            sum_d = right * (right + 1) // 2 - (left - 1) * left // 2
            sum2 += get_P(kk) * sum_d
        res = 1 - sum1 - sum2
        memo_P[m] = res
        return res

    def get_H(m, mod):
        if m == 0:
            return 0
        res = 0
        i = 1
        while i <= m:
            q = m // i
            j = min(m, m // q)
            num = j - i + 1
            sum_g = (num * (i + j) // 2) % mod
            res = (res + sum_g * (q % mod)) % mod
            i = j + 1
        return res

    segments = []
    i = 1
    while i <= N:
        q = N // i
        j = N // q
        segments.append((i, j, q))
        i = j + 1

    ans = 0
    for seg in tqdm(segments):
        i, j, q = seg
        h = get_H(q, MOD)
        h2 = (h * h) % MOD
        sum_mue = get_P(j) - get_P(i - 1)
        contrib = h2 * sum_mue
        ans += contrib

    ans = (ans % MOD + MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()