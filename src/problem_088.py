# Problem: https://projecteuler.net/problem=88
import numpy as np
from itertools import combinations

def minimal_product_sum_set(limit):
    minimal_sums = np.full(limit + 1, float('inf'))
    minimal_sums[2:] = 2 * np.arange(2, limit + 1)
    
    def find_minimal_sums(prod, sum_, start, terms):
        k = prod - sum_ + terms
        if k > limit:
            return
        if prod < minimal_sums[k]:
            minimal_sums[k] = prod
        for i in range(start, limit // prod * 2):
            find_minimal_sums(prod * i, sum_ + i, i, terms + 1)
    
    find_minimal_sums(1, 0, 2, 0)
    return minimal_sums

def main():
    limit = 12000
    minimal_sums = minimal_product_sum_set(limit)
    unique_minimal_sums = np.unique(minimal_sums[2:])
    answer = int(np.sum(unique_minimal_sums))
    return answer

if __name__ == "__main__":
    print(main())