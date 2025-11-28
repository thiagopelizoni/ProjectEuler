# Problem: https://projecteuler.net/problem=539
import numpy as np
from numba import njit

@njit(fastmath=True, cache=True)
def get_p(n, mod):
    if n == 0: return 0
    if n == 1: return 1
    if n == 2: return 2
    if n == 3: return 2
    
    path = np.zeros(64, dtype=np.int8)
    idx = 0
    temp_n = n
    while temp_n > 3:
        path[idx] = temp_n % 4
        temp_n //= 4
        idx += 1
        
    base_vals = np.array([0, 1, 2, 2], dtype=np.int64)
    res = base_vals[temp_n]
    
    for i in range(idx - 1, -1, -1):
        r = path[i]
        res = (res * 4) % mod
        if r < 2:
            res = (res - 2)
            if res < 0: res += mod
            
    return res

@njit(fastmath=True, cache=True)
def solve(limit):
    MOD = 987654321
    
    stack_n = np.zeros(64, dtype=np.int64)
    stack_k = np.zeros(64, dtype=np.int64)
    ptr = 0
    
    curr = limit
    while curr >= 4:
        k = curr // 4
        stack_n[ptr] = curr
        stack_k[ptr] = k
        ptr += 1
        curr = k - 1
        
    base_t = np.array([0, 1, 3, 5], dtype=np.int64)
    current_sum = base_t[curr]
    
    while ptr > 0:
        ptr -= 1
        n_val = stack_n[ptr]
        k_val = stack_k[ptr]
        
        term = (current_sum * 16) % MOD
        
        adj = (4 * (k_val - 1)) % MOD
        term = (term - adj)
        if term < 0: term += MOD
        
        term = (term + 5) % MOD
        
        p_k = get_p(k_val, MOD)
        
        rem = n_val % 4
        
        tail_val = (p_k * 4) % MOD
        tail_val_minus_2 = (tail_val - 2)
        if tail_val_minus_2 < 0: tail_val_minus_2 += MOD
        
        term = (term + tail_val_minus_2) % MOD
        
        if rem >= 1:
            term = (term + tail_val_minus_2) % MOD
            
        if rem >= 2:
            term = (term + tail_val) % MOD
            
        if rem == 3:
            term = (term + tail_val) % MOD
            
        current_sum = term
        
    return current_sum

def main():
    N = 10**18
    result = solve(N)
    print(result)

if __name__ == "__main__":
    main()