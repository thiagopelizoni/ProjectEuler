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
    N = 100000
    max_a = N // 3
    a_values = list(range(1, max_a + 1))
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(count_for_a, a_values, [N] * len(a_values)), total=len(a_values)))
    total_triangles = sum(results)
    print(total_triangles)

if __name__ == "__main__":
    main()