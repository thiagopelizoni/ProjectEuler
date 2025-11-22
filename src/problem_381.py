# Problem: https://projecteuler.net/problem=381
from tqdm import tqdm

def mod_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += m0
    return x

def main():
    N = 100000000
    is_prime = [True] * N
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, N, i):
                is_prime[j] = False
    primes = [p for p in range(5, N) if is_prime[p]]
    total = 0
    for p in tqdm(primes):
        inv2 = (p + 1) // 2
        inv3 = mod_inverse(3, p)
        inv6 = (inv2 * inv3) % p
        inv2_sq = (inv2 * inv2) % p
        inv8 = (inv2_sq * inv2) % p
        inv24 = (inv8 * inv3) % p
        s = (-inv2 + inv6 - inv24) % p
        total += s
    print(total)

if __name__ == "__main__":
    main()