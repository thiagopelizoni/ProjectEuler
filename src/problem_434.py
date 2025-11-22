# Problem: https://projecteuler.net/problem=434
from tqdm import tqdm

def main():
    N = 100
    MOD = 1000000033

    pof2 = [0] * ((N + 1) * (N + 1))
    pof2[0] = 1
    for i in range(1, len(pof2)):
        pof2[i] = (pof2[i - 1] * 2) % MOD

    nCr = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        nCr[n][0] = 1
        for r in range(1, n + 1):
            nCr[n][r] = (nCr[n - 1][r - 1] + nCr[n - 1][r]) % MOD

    r_val = [[0] * (N + 1) for _ in range(N + 1)]
    for i in tqdm(range(1, N + 1)):
        for j in range(N + 1):
            res = pof2[i * j]

            for a in range(1, i + 1):
                for b in range(j + 1):
                    if a == i and b == j:
                        continue

                    bin1 = nCr[i - 1][a - 1]
                    bin2 = nCr[j][b]
                    p2 = pof2[(i - a) * (j - b)]
                    rr = r_val[a][b]
                    term = bin1 * bin2 * p2 * rr % MOD
                    res = (res - term) % MOD

            r_val[i][j] = res

    s = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            s = (s + r_val[i][j]) % MOD

    print(s)

if __name__ == "__main__":
    main()