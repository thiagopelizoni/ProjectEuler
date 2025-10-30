# Problem: https://projecteuler.net/problem=467
import math
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 467 by computing f(10000) mod 1,000,000,007, where f(n) is the smallest
    positive integer that is a common superinteger of P_n and C_n. P_n is the concatenation of the first n
    digital roots of primes, and C_n for composites.

    Method / Math Rationale
    ------------------------
    Generate the first 10000 primes and composites using the Sieve of Eratosthenes.
    Compute digital roots (1 + (x - 1) % 9) and concatenate them into strings Pn and Cn.
    Use dynamic programming to compute the minimum length of a common supersequence (SCS) using a suffix
    DP table, where dp[x][y] is the min SCS length for Pn[x:] and Cn[y:].
    Construct the lexicographically smallest minimal-length SCS by greedily appending the smallest digit
    that advances at least one pointer and maintains the optimal length.
    Compute the large number represented by the SCS string modulo 1,000,000,007 iteratively to avoid
    overflow.

    Complexity
    ----------
    Time: O(n^2) for filling the DP table, where n = 10000.
    Space: O(n^2) for the DP table.

    References
    ----------
    https://projecteuler.net/problem=467
    """
    n = 10000
    MOD = 1000000007
    limit = 200000

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    primes = []
    composites = []
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
    for i in range(4, limit + 1):
        if not is_prime[i]:
            composites.append(i)

    primes = primes[:n]
    composites = composites[:n]

    def digital_root(x):
        return 1 + (x - 1) % 9

    Pn = ''.join(str(digital_root(p)) for p in primes)
    Cn = ''.join(str(digital_root(c)) for c in composites)

    A = [int(d) for d in Pn]
    B = [int(d) for d in Cn]
    na = len(A)
    nb = len(B)

    dp = [[0] * (nb + 1) for _ in range(na + 1)]

    for x in range(na + 1):
        dp[x][nb] = na - x
    for y in range(nb + 1):
        dp[na][y] = nb - y

    for x in tqdm(range(na - 1, -1, -1)):
        for y in range(nb - 1, -1, -1):
            if A[x] == B[y]:
                dp[x][y] = dp[x + 1][y + 1] + 1
            else:
                dp[x][y] = min(dp[x + 1][y], dp[x][y + 1]) + 1

    res = []
    i = 0
    j = 0
    while i < na or j < nb:
        for d_int in range(1, 10):
            new_i = i + 1 if i < na and A[i] == d_int else i
            new_j = j + 1 if j < nb and B[j] == d_int else j
            if new_i == i and new_j == j:
                continue
            if dp[i][j] == dp[new_i][new_j] + 1:
                res.append(str(d_int))
                i = new_i
                j = new_j
                break

    num = 0
    for d in res:
        num = (num * 10 + int(d)) % MOD
    print(num)

if __name__ == "__main__":
    main()