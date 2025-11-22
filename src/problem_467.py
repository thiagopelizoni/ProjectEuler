# Problem: https://projecteuler.net/problem=467
import math
from tqdm import tqdm

def main():
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