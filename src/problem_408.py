# Problem: https://projecteuler.net/problem=408
from math import isqrt
from tqdm import tqdm

def precompute_binom(max_n, mod):
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact = [0] * (max_n + 1)
    invfact[max_n] = pow(fact[max_n], mod - 2, mod)
    for i in range(max_n - 1, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % mod

    def binom(k, m):
        if m < 0 or m > k:
            return 0
        return fact[k] * invfact[m] % mod * invfact[k - m] % mod

    return binom

def main():

    n = 10000000
    mod = 1000000007
    max_sqrt = isqrt(n)
    forbidden_points = []
    for a in range(1, max_sqrt + 1):
        a2 = a * a
        for b in range(a, max_sqrt + 1):
            b2 = b * b
            sum_sq = a2 + b2
            r = isqrt(sum_sq)
            if r * r == sum_sq:
                forbidden_points.append((sum_sq, a2))
                if a != b:
                    forbidden_points.append((sum_sq, b2))

    nodes = [(0, 0, False)] + [(s, x, True) for s, x in forbidden_points] + [(2 * n, n, False)]
    nodes.sort(key=lambda t: t[0])

    binom_func = precompute_binom(2 * n, mod)

    num_nodes = len(nodes)
    dp = [0] * num_nodes
    dp[0] = 1

    for cur in tqdm(range(1, num_nodes)):
        s_cur = nodes[cur][0]
        x_cur = nodes[cur][1]
        is_bad = nodes[cur][2]
        for prev in range(cur):
            s_prev = nodes[prev][0]
            x_prev = nodes[prev][1]
            d = s_cur - s_prev
            dx = x_cur - x_prev
            if dx >= 0 and dx <= d:
                weight = binom_func(d, dx)
                contrib = (dp[prev] * weight) % mod
                if is_bad:
                    contrib = (mod - contrib) % mod
                dp[cur] = (dp[cur] + contrib) % mod

    print(dp[-1])

if __name__ == "__main__":
    main()