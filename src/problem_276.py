# Problem: https://projecteuler.net/problem=276
from tqdm import tqdm
from typing import List

def compute_h(L: int) -> int:
    if L < 1:
        return 0
    remainders: List[int] = [7, 10, 3, 10, 7, 6, 7, 10, 3, 10, 7, 6]
    period_sum: int = 86
    Q: int = L // 12
    R: int = L % 12
    sum_r: int = Q * period_sum + sum(remainders[:R])
    sum_n2: int = L * (L + 1) * (2 * L + 1) // 6
    sum_6: int = 6 * L
    return (sum_n2 + sum_6 - sum_r) // 12

def compute_d(L: int) -> int:
    if L < 3:
        return 0
    Q: int = L // 2
    num_even_k: int = Q // 2
    num_odd_k: int = (Q - 1) // 2
    sum_even: int = 0
    if num_even_k > 0:
        r: int = num_even_k
        sumk: int = r * (r + 1) // 2
        sumk2: int = r * (r + 1) * (2 * r + 1) // 6
        sum_even = (L + 1) * sumk - 4 * sumk2
    sum_odd: int = 0
    if num_odd_k > 0:
        r = num_odd_k
        sumk = r * (r + 1) // 2
        sumk2 = r * (r + 1) * (2 * r + 1) // 6
        sum_odd = (L - 1) * sumk - 4 * sumk2
    return sum_even + sum_odd

def compute_g(L: int) -> int:
    if L < 3:
        return 0
    return compute_h(L) - compute_d(L)

def main() -> None:
    M: int = 10000000
    mu: List[int] = [0] * (M + 1)
    is_comp: List[bool] = [False] * (M + 1)
    primes: List[int] = []
    mu[1] = 1
    for i in tqdm(range(2, M + 1)):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > M:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    prefix: List[int] = [0] * (M + 2)
    for i in range(1, M + 1):
        prefix[i] = prefix[i - 1] + mu[i]
    ans: int = 0
    l: int = 1
    while l <= M:
        v: int = M // l
        r: int = M // v
        musum: int = prefix[r] - prefix[l - 1]
        ans += musum * compute_g(v)
        l = r + 1
    print(ans)

if __name__ == "__main__":
    main()