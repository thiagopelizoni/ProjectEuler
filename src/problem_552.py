import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def get_primes(n):
    sieve = np.ones(n // 2, dtype=np.bool_)
    limit = int(n**0.5)
    for i in range(1, (limit - 1) // 2 + 1):
        if sieve[i]:
            sieve[2*i*(i+1)::2*i+1] = False
    count = 1
    for i in range(1, len(sieve)):
        if sieve[i]:
            count += 1
    primes = np.empty(count, dtype=np.int64)
    primes[0] = 2
    idx = 1
    for i in range(1, len(sieve)):
        if sieve[i]:
            primes[idx] = 2*i + 1
            idx += 1
    return primes

@njit(fastmath=True, cache=True)
def mod_pow(base, exp, mod):
    res = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

@njit(fastmath=True, cache=True)
def mod_inv(a, m):
    return mod_pow(a, m - 2, m)

@njit(parallel=True, fastmath=True, cache=True)
def solve_552(limit):
    primes = get_primes(limit)
    M = len(primes)
    A_mod = np.ones(M, dtype=np.int64)
    P_mod = np.empty(M, dtype=np.int64)
    for j in prange(M):
        P_mod[j] = 2 % primes[j]
    triggered = np.zeros(M, dtype=np.bool_)
    for i in range(1, M):
        p = primes[i]
        target = i + 1
        cur_A = A_mod[i]
        cur_P = P_mod[i]
        diff = target - cur_A
        if diff < 0:
            diff += p
        inv_P = mod_inv(cur_P, p)
        C = (diff * inv_P) % p
        for j in prange(i + 1, M):
            q = primes[j]
            p_val = P_mod[j]
            new_p = (p_val * p) % q
            P_mod[j] = new_p
            term = (C * p_val) % q
            new_a = A_mod[j] + term
            if new_a >= q:
                new_a -= q
            A_mod[j] = new_a
            if new_a == 0:
                triggered[j] = True
    total_sum = 0
    for i in range(M):
        if triggered[i]:
            total_sum += primes[i]
    return total_sum

def main():
    LIMIT = 300000
    print(solve_552(LIMIT))

if __name__ == "__main__":
    main()