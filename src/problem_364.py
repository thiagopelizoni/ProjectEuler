# Problem: https://projecteuler.net/problem=364
from tqdm import tqdm

def main():
    def mod_binom(p, q, mod):
        if q < 0 or q > p:
            return 0
        return fact[p] * pow(fact[q], mod - 2, mod) % mod * pow(fact[p - q], mod - 2, mod) % mod

    N = 1000000
    MOD = 100000007
    fact = [1] * (N + 2)
    for i in tqdm(range(1, N + 2)):
        fact[i] = fact[i - 1] * i % MOD
    r = 0
    for v in range(3):
        target = N - 1 - v
        mult = 1 + (1 if v == 1 else 0)
        for m in range(target // 2 + 1):
            temp = target - 2 * m
            if temp % 3 == 0:
                k = temp // 3
                if k >= 0:
                    term = fact[m + k + 1] * mod_binom(m + k, m, MOD) * pow(2, k, MOD) * fact[k + v] * fact[m + k] % MOD
                    r = (r + term * mult % MOD) % MOD
    print(r)

if __name__ == "__main__":
    main()