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
    """
    Purpose
    -------
    Compute the number of hidden points H(n) in a hexagonal orchard of order n,
    where n=100_000_000, as defined in Project Euler problem 351.

    Method / Math Rationale
    -----------------------
    Due to the six-fold symmetry of the hexagon, the problem can be reduced to
    analyzing one-sixth of the structure. Points hidden from the center are
    those along rays where the coordinates are not coprime. For each "ring" i
    from 1 to n, the number of hidden points is 6 * (i - phi(i)), where phi is
    Euler's totient function. Thus, H(n) = 6 * (sum_{i=1}^n i - sum_{i=1}^n
    phi(i)) = 3 * n * (n + 1) - 6 * sum_{i=1}^n phi(i). The sum of phi(i) is
    computed efficiently using a sieve-like algorithm similar to the Sieve of
    Eratosthenes.

    Complexity
    ----------
    Time: O(n log log n) due to the harmonic sum in the sieve updates.
    Space: O(n) for the phi array.

    References
    ----------
    https://projecteuler.net/problem=351
    """
    n = 100000000
    sum_phi = compute_sum_phi(n)
    tri = n * (n + 1) // 2
    h = 6 * (tri - sum_phi)
    print(h)

if __name__ == "__main__":
    main()