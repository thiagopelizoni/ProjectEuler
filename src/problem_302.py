# Problem: https://projecteuler.net/problem=302
import numpy as np
from numba import njit, prange
import math

LIMIT = 10**18
MAX_PRIME = 1000000 

@njit(fastmath=True, cache=True)
def get_sieve(n):
    spf = np.arange(n + 1, dtype=np.int32)
    spf[0] = 0
    spf[1] = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if spf[i] == i:
            for j in range(i*i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    
    primes = []
    for i in range(2, n + 1):
        if spf[i] == i:
            primes.append(i)
            
    return np.array(primes, dtype=np.int64), spf

@njit(fastmath=True)
def update_phi_counts(counts, p, k, spf, direction):
    if k > 1:
        counts[p] += (k - 1) * direction

    temp = p - 1
    while temp > 1:
        f = spf[temp]
        counts[f] += direction
        temp //= f

@njit(fastmath=True)
def is_phi_achilles(phi_counts, max_touched_prime):
    g = 0
    for i in range(2, max_touched_prime + 1):
        c = phi_counts[i]
        if c == 0:
            continue
        if c == 1:
            return False
        
        if g == 0:
            g = c
        else:
            g = math.gcd(g, c)
    
    return g == 1

@njit(fastmath=True)
def dfs(prime_idx, current_val, current_n_gcd, phi_counts, primes, spf, max_touched_prime):
    count = 0
    n_primes = len(primes)
    
    for i in range(prime_idx, n_primes):
        p = primes[i]
        
        p_sq = p * p
        
        if current_val > LIMIT // p_sq:
            break

        current_val_with_p = current_val * p_sq
        k = 2
        
        new_max_touched = p if p > max_touched_prime else max_touched_prime
        
        while True:
            if current_val_with_p > LIMIT:
                break
            
            update_phi_counts(phi_counts, p, k, spf, 1)
            new_n_gcd = math.gcd(current_n_gcd, k)
            
            if new_n_gcd == 1 and k >= 3:
                if is_phi_achilles(phi_counts, new_max_touched):
                    count += 1
            
            if i + 1 < n_primes:
                next_p = primes[i+1]
                if current_val_with_p <= LIMIT // (next_p * next_p):
                    count += dfs(i + 1, current_val_with_p, new_n_gcd, phi_counts, primes, spf, new_max_touched)
            
            update_phi_counts(phi_counts, p, k, spf, -1)
            
            if current_val_with_p > LIMIT // p:
                break
            current_val_with_p *= p
            k += 1
            
    return count

@njit(parallel=True, fastmath=True)
def driver():
    primes, spf = get_sieve(MAX_PRIME)
    n_primes = len(primes)
    total_count = 0
    
    for i in prange(n_primes):
        p = primes[i]
        p_sq = p * p
        if p_sq > LIMIT:
            continue
            
        phi_counts = np.zeros(MAX_PRIME + 1, dtype=np.int32)
        
        current_val = 1
        val_pow = p_sq
        k = 2
        
        local_count = 0
        
        while True:
            next_val = val_pow
            if next_val > LIMIT:
                break
                
            update_phi_counts(phi_counts, p, k, spf, 1)
            
            curr_gcd = k
            
            max_touched = p
            
            if i + 1 < n_primes:
                next_p = primes[i+1]
                if next_val <= LIMIT // (next_p * next_p):
                    local_count += dfs(i + 1, next_val, curr_gcd, phi_counts, primes, spf, max_touched)
            
            update_phi_counts(phi_counts, p, k, spf, -1)
            
            if next_val > LIMIT // p:
                break
            val_pow *= p
            k += 1
            
        total_count += local_count
        
    return total_count

def main():
    result = driver()
    print(result)

if __name__ == "__main__":
    main()