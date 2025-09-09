# Problem: https://projecteuler.net/problem=296
import math
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def count_for_a(a: int, N: int) -> int:
    total = 0
    max_b = (N - a) // 2
    for b in range(a, max_b + 1):
        g = math.gcd(a, b)
        ab_sum = a + b
        e = ab_sum // g
        min_c = b
        max_c = min(ab_sum - 1, N - ab_sum)
        if max_c < min_c:
            continue

        m_min = (min_c + e - 1) // e
        m_max = max_c // e
        if m_max >= m_min:
            total += m_max - m_min + 1

    return total

def main():
    """
    Purpose:
    Solves Project Euler problem 296: Counts the number of integer-sided triangles ABC with sides a=BC, b=AC, c=AB where
    a <= b <= c, perimeter a + b + c <= 100000, and the length BE is an integer, where BE is defined as per the problem
    involving the angular bisector and tangent.

    Method / Math Rationale:
    For each possible a and b (with a <= b), compute g = gcd(a, b), e = (a + b) // g. Then, c must be a multiple of e in
    the range [b, min(a + b - 1, 100000 - a - b)]. The condition BE = a * c / (a + b) being integer is equivalent to e
    dividing c. Count such c for each a, b using ceiling and floor to find the number of multiples.

    Complexity:
    O(M * K) where M ~ 33333, K ~ 25000 on average, leading to ~8.5e8 operations, parallelized over available CPUs for
    efficiency.

    References:
    https://projecteuler.net/problem=296
    """
    N = 100000
    max_a = N // 3
    a_values = list(range(1, max_a + 1))
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(count_for_a, a_values, [N] * len(a_values)), total=len(a_values)))
    total_triangles = sum(results)
    print(total_triangles)

if __name__ == "__main__":
    main()