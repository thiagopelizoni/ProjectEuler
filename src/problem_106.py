# Problem: https://projecteuler.net/problem=106
from itertools import combinations

def necessary_tests(n):
    def is_comparison_necessary(B, C):
        return any(b > c for b, c in zip(B, C))

    count = 0

    elements = list(range(1, n + 1))
    for i in range(1, n // 2 + 1):  # Subset sizes from 1 to n/2 (rounded down)
        for B in combinations(elements, i):
            for C in combinations([x for x in elements if x not in B], i):
                if B[0] < C[0] and is_comparison_necessary(B, C):
                    count += 1
    return count

print(necessary_tests(12))
