# Problem: https://projecteuler.net/problem=278
from typing import List
from sympy.ntheory.generate import primerange

def main() -> None:
    primes: List[int] = list(primerange(2, 5000))
    n: int = len(primes)
    s1: int = 0
    s2: int = 0
    s3: int = 0
    for p in primes:
        s1 += p
        s2 += p * p
        s3 += p * p * p
    sum_pqr: int = (s1 * s1 * s1 - 3 * s1 * s2 + 2 * s3) // 6
    prefix_sum: List[int] = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + primes[i]
    sum_pq: int = 0
    for j in range(1, n - 1):
        sum_pq += primes[j] * (n - j - 1) * prefix_sum[j]
    suffix_sum: List[int] = [0] * (n + 1)
    suffix_p_times_idx: List[int] = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + primes[i]
        suffix_p_times_idx[i] = suffix_p_times_idx[i + 1] + primes[i] * i
    sum_pr: int = 0
    for i in range(n - 2):
        temp: int = suffix_p_times_idx[i + 2] - (i + 1) * suffix_sum[i + 2]
        sum_pr += primes[i] * temp
    sum_qr: int = 0
    for j in range(1, n - 1):
        sum_qr += primes[j] * j * suffix_sum[j + 1]
    ans: int = 2 * sum_pqr - (sum_pq + sum_pr + sum_qr)
    print(ans)

if __name__ == "__main__":
    main()