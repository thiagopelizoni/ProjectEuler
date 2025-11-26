# Problem: https://projecteuler.net/problem=532
import numpy as np
from numba import njit
import math

@njit(fastmath=True, cache=True)
def integrand(phi, k):
    s = math.sin(phi)
    return math.sqrt(s*s + k*k) / s

@njit(fastmath=True, cache=True)
def simpson_integration(n):
    k = 1.0 / math.tan(math.pi / n)
    a = math.acos(0.999)
    b = math.pi / 2.0
    steps = 200000
    h = (b - a) / steps
    
    total = integrand(a, k) + integrand(b, k)
    
    sum_odd = 0.0
    for i in range(1, steps, 2):
        sum_odd += integrand(a + i * h, k)
        
    sum_even = 0.0
    for i in range(2, steps, 2):
        sum_even += integrand(a + i * h, k)
        
    return (h / 3.0) * (total + 4.0 * sum_odd + 2.0 * sum_even)

@njit(fastmath=True, cache=True)
def solve_problem():
    target_length = 1000.0
    n = 300
    
    while True:
        length = simpson_integration(n)
        if length > target_length:
            return n * length
        n += 1

def main():
    result = solve_problem()
    print(f"{result:.2f}")

if __name__ == "__main__":
    main()