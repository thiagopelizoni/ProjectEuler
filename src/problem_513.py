# Problem: https://projecteuler.net/problem=513
from concurrent.futures import ProcessPoolExecutor
from math import sqrt
from tqdm import tqdm
import numba

@numba.jit(nopython=True)
def is_square(x):
    if x <= 0:
        return False
    s = int(sqrt(x))
    return s * s == x

@numba.jit(nopython=True)
def count_for_g(g):
    c = 2 * g
    count = 0
    for b in range(g + 1, c + 1):
        min_a = max(1, c + 1 - b)
        if b % 2 == 0:
            start_a = min_a if min_a % 2 == 0 else min_a + 1
        else:
            start_a = min_a if min_a % 2 == 1 else min_a + 1
        for a in range(start_a, b + 1, 2):
            num = 2 * a * a + 2 * b * b - c * c
            val = num // 4
            if is_square(val):
                count += 1
    return count

def main():
    """
    Purpose
    -------
    Computes the number of integral-sided triangles with sides a <= b <= c <= 100000 such that the median from the vertex
    opposite side c to the midpoint of side c is an integer length. No parameters. Prints the count.

    Method / Math Rationale
    ---------------------
    Enumerates all possible even c = 2*g, and for each g, enumerates all possible a <= b <= c with a + b > c and a, b same parity.
    For each, computes val = (2*a**2 + 2*b**2 - c**2) / 4 and checks if it is a perfect square using integer square root.

    Complexity
    ----------
    O(n^3) time, O(1) space excluding parallel overhead.

    References
    ----------
    https://projecteuler.net/problem=513
    """
    n = 100000
    max_g = n // 2
    total = 0
    with ProcessPoolExecutor() as executor:
        for count in tqdm(executor.map(count_for_g, range(1, max_g + 1)), total=max_g):
            total += count
    print(total)

if __name__ == "__main__":
    main()