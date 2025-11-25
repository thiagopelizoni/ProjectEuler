# Problem: https://projecteuler.net/problem=523
import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True, cache=True)
def compute_expected_cost(n: int) -> float:
    total_sum = 0.0
    for k in prange(2, n + 1):
        numerator = 2.0 ** (k - 1) - 1.0
        term = numerator / k
        total_sum += term
    return total_sum

def main():
    n = 30
    _ = compute_expected_cost(5)
    result = compute_expected_cost(n)
    print(f"{result:.2f}")

if __name__ == "__main__":
    main()