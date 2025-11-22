# Problem: https://projecteuler.net/problem=517
import math
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def mod_comb(m, k, fact, invfact, mod):
    if m < k or k < 0 or m < 0:
        return 0
    return fact[m] * invfact[k] % mod * invfact[m - k] % mod

def compute_G(p, mod, fact, invfact):
    total = 0
    k = 0
    while True:
        kk_p = k * k * p
        floor_ks = math.isqrt(kk_p)
        m = p + k - floor_ks - 1
        if m < k:
            break
        total = (total + mod_comb(m, k, fact, invfact, mod)) % mod
        k += 1
    return total

def get_primes_in_range(low, high):
    sqrt_high = int(math.sqrt(high)) + 1
    sieve = [True] * (sqrt_high + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(sqrt_high)) + 1):
        if sieve[i]:
            for j in range(i * i, sqrt_high + 1, i):
                sieve[j] = False
    small_primes = [i for i in range(2, sqrt_high + 1) if sieve[i]]
    size = high - low + 1
    is_prime = [True] * size
    for sp in small_primes:
        start = max(sp * sp, ((low + sp - 1) // sp) * sp)
        for mul in range(start, high + 1, sp):
            if mul >= low:
                is_prime[mul - low] = False
    primes = [low + i for i in range(size) if is_prime[i]]
    return primes

def compute_wrapper(arg):
    return compute_G(*arg)

def main():
    MOD = 1000000007
    MAX = 10010000
    fact = [1] * (MAX + 1)
    for i in tqdm(range(1, MAX + 1)):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [0] * (MAX + 1)
    invfact[MAX] = pow(fact[MAX], MOD - 2, MOD)
    for i in range(MAX - 1, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD
    low = 10000001
    high = 10009999
    primes = get_primes_in_range(low, high)
    args = [(p, MOD, fact, invfact) for p in primes]
    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_wrapper, args)
    total_sum = sum(results) % MOD
    print(total_sum)

if __name__ == "__main__":
    main()