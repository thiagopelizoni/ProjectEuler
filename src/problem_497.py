# Problem: https://projecteuler.net/problem=497
from tqdm import tqdm

def dist(p_mod, g_mod, k_mod, mod, p_less_g):
    if p_less_g:
        diff = (g_mod - p_mod) % mod
        sum_m2 = (g_mod + p_mod - 2) % mod
        return (diff * sum_m2) % mod
    else:
        diff = (p_mod - g_mod) % mod
        d2 = (2 * k_mod - p_mod - g_mod) % mod
        return (diff * d2) % mod

def main():
    mod = 1000000000
    total = 0
    for n in tqdm(range(1, 10001)):
        A = pow(3, n, mod)
        B = pow(6, n, mod)
        C = pow(9, n, mod)
        K = pow(10, n, mod)
        pos = [A, B, C]
        dp = [[[[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(n + 1)]
        for d in range(1, n + 1):
            for f in range(3):
                for t in range(3):
                    if t == f:
                        continue
                    for v in range(3):
                        if v == f or v == t:
                            continue
                        for s in range(3):
                            if d == 1:
                                dist1 = 0
                                end_sub1 = s
                                dist2 = 0
                            else:
                                dist1 = dp[d - 1][f][v][t][s]
                                end_sub1 = v
                                dist2 = dp[d - 1][v][t][f][t]
                            trans1 = dist(pos[end_sub1], pos[f], K, mod, end_sub1 < f)
                            trans2 = dist(pos[f], pos[t], K, mod, f < t)
                            val = (dist1 + trans1 + trans2 + dist2) % mod
                            dp[d][f][t][v][s] = val
        e = dp[n][0][2][1][1]
        total = (total + e) % mod
    print(total)

if __name__ == "__main__":
    main()