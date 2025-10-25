# Problem: https://projecteuler.net/problem=455
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def find_fixed_point(n, modulo=1000000000):
    exponent = n
    while True:
        next_exp = pow(n, exponent, modulo)
        if next_exp == 0 or next_exp == exponent:
            return next_exp
        exponent = next_exp

def main():
    """
    Purpose
    -------
    Computes and prints the sum of f(n) for n from 2 to 10^6, where f(n) is the largest
    positive integer x less than 10^9 such that the last 9 digits of n^x form x
    (including leading zeros), or 0 if no such x exists, as per Project Euler problem 455.
    Parameters: None
    Returns: None

    Method / Math Rationale
    -----------------------
    For each n, iterate the map x -> n^x mod 10^9 starting from x = n until a fixed point
    is reached (where n^x mod 10^9 = x) or 0. This empirically finds the required x.
    Computations are parallelized using ProcessPoolExecutor for efficiency.

    Complexity
    ----------
    O(10^6 * I * log(10^9)) where I is the number of iterations per n (small, ~10-20).
    With parallelism, runtime is reduced proportionally to the number of CPU cores.

    References
    ----------
    https://projecteuler.net/problem=455
    """
    limit = 1000000
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(find_fixed_point, range(2, limit + 1)), total=limit - 1))
    print(sum(results))

if __name__ == "__main__":
    main()