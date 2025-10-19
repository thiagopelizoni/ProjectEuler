# Problem: https://projecteuler.net/problem=434
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Compute S(100), the sum of R(i, j) for 1 <= i, j <= 100, where R(m, n) is the number of
    ways to make an m x n grid graph rigid by adding diagonals, modulo 1000000033.
    No parameters.
    Returns: None (prints the result).

    Method / Math Rationale
    -----------------------
    Uses dynamic programming to compute R(i, j) using the formula for the number of connected
    bipartite graphs between sets of sizes i and j:
    R(i, j) = 2^{i*j} - sum over 1 <= a <= i, 0 <= b <= j (excluding a=i and b=j) of
    binom(i-1, a-1) * binom(j, b) * 2^{(i-a)*(j-b)} * R(a, b).
    This counts the connected labeled bipartite graphs, corresponding to rigid configurations
    where each cell may or may not have a diagonal (orientation not distinguished).

    Complexity
    ----------
    Time: O(N^4) due to DP with O(N^2) states and O(N^2) work per state.
    Space: O(N^2).

    References
    ----------
    https://projecteuler.net/problem=434
    """
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