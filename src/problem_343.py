# Problem: https://projecteuler.net/problem=343
from concurrent.futures import ProcessPoolExecutor
from sympy.ntheory import factorint
from tqdm import tqdm

def compute_f(k):
    a = k + 1
    factors_a = factorint(a)
    lpf_a = max(factors_a.keys())
    b = k * k - k + 1
    factors_b = factorint(b)
    lpf_b = max(factors_b.keys()) if factors_b else 0
    max_lpf = max(lpf_a, lpf_b)
    return max_lpf - 1

def main():
    """
    Purpose
    -------
    Computes the sum of f(k^3) for k from 1 to 2,000,000, where f is the terminal integer
    in the fractional sequence defined in Project Euler problem 343.

    Method / Math Rationale
    -----------------------
    The function f(m) equals the largest prime factor of (m + 1) minus 1. Since m = k^3,
    m + 1 = (k + 1)(k^2 - k + 1). Thus, for each k, factorize both components to find
    the overall largest prime factor, subtract 1 to get f(k^3), and sum over all k.

    Complexity
    ----------
    O(N * T), where N = 2e6 and T is the average time for factorint on numbers up to 4e12,
    parallelized across available CPUs.

    References
    ----------
    https://projecteuler.net/problem=343
    """
    N = 2000000
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(compute_f, range(1, N + 1)), total=N))
    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()