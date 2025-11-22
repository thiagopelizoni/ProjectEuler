# Problem: https://projecteuler.net/problem=320
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import math
import numpy as np

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def compute_s_for_p(p, M):
    s = [0] * (M + 1)
    current = 0
    for i in range(1, M + 1):
        current += 1
        if (i - 1) % p == p - 1:
            t = 1
            temp = (i - 1) // p
            while temp % p == p - 1:
                t += 1
                temp //= p
            current -= (p - 1) * t
        s[i] = current
    return s

def valuation(n, p):
    if n < p:
        return 0
    v = 0
    power = p
    while power <= n:
        v += n // power
        next_power = power * p
        if next_power > n or next_power <= 0:
            break
        power = next_power
    return v

def find_min_n(p, e, T):
    if e == 0:
        return 0
    low = T
    if p > 2:
        log_approx = (T.bit_length() * math.log(2)) / math.log(p)
    else:
        log_approx = T.bit_length()
    num_digits = int(log_approx) + 1
    high = T + (p - 1) * (num_digits + 20)
    while low < high:
        mid = low + (high - low) // 2
        if valuation(mid, p) >= e:
            high = mid
        else:
            low = mid + 1
    return low

def main():
    k = 1234567890
    M = 1000000
    MOD = 10**18
    LIMIT = int(math.sqrt(M)) + 100  # ~1100
    MAX_K = 100

    primes = sieve(M)
    prime_set = set(primes)
    small_primes = [p for p in primes if p <= LIMIT]

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_s_for_p, p, M) for p in small_primes]
        s_arrays = [f.result() for f in futures]

    prev_prime = [0] * (M + 1)
    current_prime = 0
    for i in range(2, M + 1):
        if i in prime_set:
            current_prime = i
        prev_prime[i] = current_prime

    total = 0
    for i in tqdm(range(10, M + 1), total=M-9):
        # min_s_small
        min_s_small = min(s_arrays[j][i] for j in range(len(small_primes)) if small_primes[j] <= i)

        # large contributions via k
        min_s_large = float('inf')
        large_cand_s = {}
        for kk in range(1, min(MAX_K, min_s_small + 1)):
            m = i // kk
            if m < 2:
                continue
            p = prev_prime[m]
            if p <= LIMIT or p < 2:
                continue
            if i // p == kk:
                s = i - kk * (p - 1)
                if s < min_s_large:
                    min_s_large = s
                    large_cand_s = {p: s}
                elif s == min_s_large:
                    large_cand_s[p] = s

        overall_min_s = min(min_s_small, min_s_large) if min_s_large != float('inf') else min_s_small

        candidates = []
        for j in range(len(small_primes)):
            pp = small_primes[j]
            if pp > i:
                break
            if s_arrays[j][i] == overall_min_s:
                candidates.append(pp)
        if min_s_large == overall_min_s:
            candidates.extend(large_cand_s.keys())

        diff = i - overall_min_s
        T = k * diff
        max_d = 0
        for p in candidates:
            v_i = diff // (p - 1)
            e = k * v_i
            n_p = find_min_n(p, e, T)
            d = n_p - T
            if d > max_d:
                max_d = d

        N_mod = ( (k * diff % MOD) + max_d ) % MOD
        total = (total + N_mod) % MOD

    print(total)

if __name__ == "__main__":
    main()