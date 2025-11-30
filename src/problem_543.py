# Problem: https://projecteuler.net/problem=543
import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def get_fib_sequence(max_k):
    fibs = np.zeros(max_k + 1, dtype=np.int64)
    fibs[1] = 1
    fibs[2] = 1
    for i in range(3, max_k + 1):
        fibs[i] = fibs[i-1] + fibs[i-2]
    return fibs

@njit(parallel=True, fastmath=True, cache=True)
def get_primes(n):
    size = (n + 1) // 2
    sieve = np.ones(size, dtype=np.bool_)
    sieve[0] = False
    
    limit = int(n**0.5)
    sqrt_lim_idx = (limit + 1) // 2
    
    for i in range(1, sqrt_lim_idx):
        if sieve[i]:
            val = 2 * i + 1
            start_idx = (val * val) // 2
            sieve[start_idx::val] = False
            
    count = 1
    for i in prange(1, size):
        if sieve[i]:
            count += 1
            
    primes = np.empty(count, dtype=np.int32)
    primes[0] = 2
    
    idx = 1
    for i in range(1, size):
        if sieve[i]:
            primes[idx] = 2 * i + 1
            idx += 1
            
    return primes

@njit(fastmath=True, cache=True)
def prime_pi_fast(n, primes):
    if n < 2: return 0
    return np.searchsorted(primes, n, side='right')

@njit(fastmath=True, cache=True)
def calculate_S(n, primes):
    if n < 2: return 0
    
    term1 = prime_pi_fast(n, primes)
    
    term2_even = (n // 2) - 1
    
    pi_n_minus_2 = prime_pi_fast(n - 2, primes)
    term2_odd = 0
    if pi_n_minus_2 > 0:
        term2_odd = pi_n_minus_2 - 1
    if term2_odd < 0: term2_odd = 0
    
    term2 = term2_even + term2_odd
    
    term3 = 0
    if n >= 6:
        m = n // 2
        if n % 2 == 0:
            term3 = (m - 2) * (m - 2)
        else:
            term3 = (m - 1) * (m - 2)
        
    return term1 + term2 + term3

@njit(fastmath=True)
def solve_problem():
    max_k = 44
    fibs = get_fib_sequence(max_k)
    max_n = fibs[max_k]
    
    primes = get_primes(max_n)
    
    total_sum = 0
    for k in range(3, max_k + 1):
        n = fibs[k]
        total_sum += calculate_S(n, primes)
        
    return total_sum

def main():
    result = solve_problem()
    print(result)

if __name__ == "__main__":
    main()