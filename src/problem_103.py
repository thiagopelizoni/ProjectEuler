# Problem: https://projecteuler.net/problem=103
from itertools import combinations

def is_special_sum_set(s):
    for m in range(1, len(s) // 2 + 1):
        if sum(sorted(s)[:m+1]) <= sum(sorted(s)[-m:]):
            return False
    sums = set()
    for r in range(1, len(s)):
        for comb in combinations(s, r):
            if sum(comb) in sums:
                return False
            sums.add(sum(comb))
    return True

def find_optimum_special_sum_set(n):
    best_set = None
    best_sum = float('inf')
    initial_set = [i for i in range(1, n + 1)]
    for comb in combinations(range(1, 50), n):
        if sum(comb) < best_sum and is_special_sum_set(comb):
            best_set = comb
            best_sum = sum(comb)
    return best_set

if __name__ == "__main__":
    optimum_set = find_optimum_special_sum_set(7)
    answer = ''.join(map(str, optimum_set))
    print(answer)
