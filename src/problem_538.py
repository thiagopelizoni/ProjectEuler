# Problem: https://projecteuler.net/problem=538
import numpy as np
from numba import njit

@njit(fastmath=True, cache=True)
def count_set_bits(n):
    c = 0
    while n > 0:
        n &= (n - 1)
        c += 1
    return c

@njit(fastmath=True, cache=True)
def get_area(a, b, c, d):
    s = (a + b + c + d) * 0.5
    val = (s - a) * (s - b) * (s - c) * (s - d)
    return np.sqrt(val) if val > 0 else 0.0

@njit(cache=True)
def solve():
    limit = 3000000
    p2 = np.array([2**i for i in range(32)], dtype=np.int64)
    p3 = np.array([3**i for i in range(32)], dtype=np.int64)
    
    K = 40
    top = np.zeros(K, dtype=np.int64)
    size = 0
    
    total_peri_sum = 0
    
    for n in range(1, limit + 1):
        b3 = count_set_bits(3 * n)
        b2 = count_set_bits(2 * n)
        b1 = count_set_bits(n + 1)
        
        u = p2[b3] + p3[b2] + b1
        
        if size < K:
            top[size] = u
            size += 1
            curr = size - 1
            while curr > 0 and top[curr] > top[curr-1]:
                top[curr], top[curr-1] = top[curr-1], top[curr]
                curr -= 1
        else:
            if u > top[K-1]:
                top[K-1] = u
                curr = K - 1
                while curr > 0 and top[curr] > top[curr-1]:
                    top[curr], top[curr-1] = top[curr-1], top[curr]
                    curr -= 1
        
        if n >= 4:
            max_area = -1.0
            max_peri = 0
            
            for i in range(size - 3):
                a, b, c, d = top[i], top[i+1], top[i+2], top[i+3]
                
                if a < b + c + d:
                    area = get_area(a, b, c, d)
                    
                    if area > max_area:
                        max_area = area
                        max_peri = a + b + c + d
                    elif area == max_area:
                        peri = a + b + c + d
                        if peri > max_peri:
                            max_peri = peri
                            
            total_peri_sum += max_peri
            
    return total_peri_sum

def main():
    print(solve())

if __name__ == "__main__":
    main()