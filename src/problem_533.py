# Problem: https://projecteuler.net/problem=533
import numpy as np
from numba import njit
import math

@njit(fastmath=True, cache=True)
def solve_optimized():
    LIMIT = 20_000_000
    MOD = 1_000_000_000
    
    weights = np.zeros(LIMIT, dtype=np.float64)
    
    log2 = math.log(2)
    
    weights[:] += log2
    
    weights[2::2] += 2.0 * log2
    
    curr = 4
    while curr < LIMIT:
        weights[curr::curr] += log2
        curr *= 2

    is_prime = np.ones(LIMIT, dtype=np.bool_)
    is_prime[0] = False
    is_prime[1] = False
    
    sqrt_lim = int(math.sqrt(LIMIT))
    for i in range(2, sqrt_lim + 1):
        if is_prime[i]:
            for j in range(i*i, LIMIT, i):
                is_prime[j] = False
                
    for p in range(3, LIMIT):
        if is_prime[p]:
            d = p - 1
            if d >= LIMIT: 
                break
                
            log_p = math.log(p)
            
            curr = d
            while curr < LIMIT:
                for j in range(curr, LIMIT, curr):
                    weights[j] += log_p
                if curr > (LIMIT // p):
                    break
                curr *= p

    best_L = 0
    max_w = -1.0
    for i in range(1, LIMIT):
        if weights[i] > max_w:
            max_w = weights[i]
            best_L = i
            
    result = 1
    
    if best_L % 2 != 0:
        result = (result * 2) % MOD
    else:
        v2 = 0
        temp = best_L
        while (temp & 1) == 0:
            v2 += 1
            temp >>= 1
            
        exponent = v2 + 2
        
        term = 1
        base = 2
        e_loop = exponent
        while e_loop > 0:
            if e_loop % 2 == 1:
                term = (term * base) % MOD
            base = (base * base) % MOD
            e_loop //= 2
        result = (result * term) % MOD
        
    for p in range(3, LIMIT):
        if is_prime[p]:
            d = p - 1
            if d > best_L:
                break
            
            if best_L % d == 0:
                target = best_L // d
                e_minus_1 = 0
                while target > 0 and target % p == 0:
                    e_minus_1 += 1
                    target //= p
                
                exponent = e_minus_1 + 1
                
                term = 1
                base = p
                e_loop = exponent
                while e_loop > 0:
                    if e_loop % 2 == 1:
                        term = (term * base) % MOD
                    base = (base * base) % MOD
                    e_loop //= 2
                
                result = (result * term) % MOD

    return (result + 1) % MOD

def main():
    ans = solve_optimized()
    print(ans)

if __name__ == "__main__":
    main()