# Problem: https://projecteuler.net/problem=351
import numpy as np
from numba import njit
from tqdm import tqdm

@njit
def update_multiples(phi, i, n):
    for j in range(i, n + 1, i):
        phi[j] = (phi[j] // i) * (i - 1)

def compute_sum_phi(n):
    phi = np.arange(n + 1, dtype=np.uint64)
    for i in tqdm(range(2, n + 1)):
        if phi[i] == i:
            update_multiples(phi, i, n)
    return np.sum(phi)

def main():
    n = 100000000
    sum_phi = compute_sum_phi(n)
    tri = n * (n + 1) // 2
    h = 6 * (tri - sum_phi)
    print(h)

if __name__ == "__main__":
    main()