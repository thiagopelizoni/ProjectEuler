# Problem: https://projecteuler.net/problem=527
import numpy as np
from numba import njit
import math

@njit(fastmath=True, cache=True)
def solve():
    n = 10**10
    k = int(math.log2(n))
    nodes_full = (1 << k) - 1
    nodes_leaves = n - nodes_full
    sum_full_depths = (k - 1) * (1 << k) + 1
    sum_leaf_depths = nodes_leaves * (k + 1)
    B_n = (sum_full_depths + sum_leaf_depths) / n
    gamma = 0.577215664901532860606512
    ln_n = math.log(n)
    inv_n = 1.0 / n
    H_n = ln_n + gamma + (0.5 * inv_n) - (inv_n * inv_n / 12.0)
    R_n = 2.0 * (1.0 + inv_n) * H_n - 3.0
    return R_n - B_n

def main():
    result = solve()
    print(f"{result:.8f}")

if __name__ == "__main__":
    main()