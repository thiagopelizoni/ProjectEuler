# Problem: https://projecteuler.net/problem=73
from math import gcd

def count_fractions_in_range(min_n, max_n, d_max):
    count = 0
    for d in range(2, d_max + 1):
        n_min = d // 3 + 1
        n_max = d // 2

        for n in range(n_min, n_max + 1):
            if gcd(n, d) == 1:
                if min_n < n / d < max_n:
                    count += 1
    return count

if __name__ == "__main__":
    min_n = 1 / 3
    max_n = 1 / 2
    d_max = 12_000
    answer = count_fractions_in_range(min_n, max_n, 12000)
    print(answer)
