import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def get_spf(limit):
    spf = np.arange(limit + 1, dtype=np.int32)
    for i in range(2, int(limit**0.5) + 1):
        if spf[i] == i:
            for j in range(i*i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

@njit(fastmath=True)
def get_prime_factors(n, spf, buffer):
    cnt = 0
    curr = n
    while curr > 1:
        p = spf[curr]
        buffer[cnt] = p
        cnt += 1
        while curr % p == 0:
            curr //= p
    return cnt

@njit(fastmath=True)
def count_coprime(limit, factors, count):
    res = 0
    n_subsets = 1 << count
    
    for i in range(n_subsets):
        divisor = 1
        set_bits = 0
        temp = i
        idx = 0
        
        while temp > 0:
            if temp & 1:
                divisor *= factors[idx]
                set_bits += 1
            idx += 1
            temp >>= 1
            
        term = limit // divisor
        
        if set_bits & 1:
            res -= term
        else:
            res += term
            
    return res

@njit(parallel=True, fastmath=True, cache=True)
def solve_kernel(N, spf):
    m_limit = int(np.sqrt(N))
    total_count = 0
    
    for m in prange(2, m_limit + 1):
        m_sq = m * m
        if m_sq >= N:
            continue
            
        max_n_geom = int(np.sqrt(N - m_sq))
        limit_n = min(m - 1, max_n_geom)
        
        if limit_n < 1:
            continue
            
        search_limit = 0
        if m % 2 == 0:
            search_limit = limit_n
        else:
            search_limit = limit_n // 2
            
        if search_limit == 0:
            continue
            
        factors = np.zeros(10, dtype=np.int64)
        n_factors = get_prime_factors(m, spf, factors)
        
        c = count_coprime(search_limit, factors, n_factors)
        total_count += c
        
    return total_count

def main():
    N = 3141592653589793
    
    limit_m = int(N**0.5) + 100
    
    spf = get_spf(limit_m)
    
    result = solve_kernel(N, spf)
    print(result)

if __name__ == "__main__":
    main()