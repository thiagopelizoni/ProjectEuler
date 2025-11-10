# Problem: https://projecteuler.net/problem=491
from itertools import combinations
from math import factorial
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 491: count the number of double pandigital numbers divisible by 11.

    Method / Math Rationale
    ------------------------
    Enumerates canonical bitmasks for multisets in odd positions using combinations, skipping invalid patterns.
    Computes sum of digits in odd positions, checks if (90 - 2 * sum_odd) % 11 == 0.
    Adds squared multinomial coefficient for arrangements in odd and even positions.
    Multiplies total by 9/10 to exclude leading zeros, as the fraction is exactly 1/10.

    Complexity
    ----------
    O(C(20,10)) time, which is about 184756 iterations, constant space.

    References
    ----------
    https://projecteuler.net/problem=491
    """
    n = 10
    num_digits = 20
    digit_sum = 90
    fact10 = factorial(10)
    perm_repeated = [fact10 // (1 << i) for i in range(n + 1)]
    result = 0
    for selected in tqdm(list(combinations(range(num_digits), n))):
        ok = True
        for d in range(n):
            first = 2 * d
            second = 2 * d + 1
            has_first = first in selected
            has_second = second in selected
            if not has_first and has_second:
                ok = False
                break
        if not ok:
            continue
        sum_odd = sum(pos // 2 for pos in selected)
        repeated = sum(1 for pos in selected if pos % 2 == 1)
        diff = digit_sum - 2 * sum_odd
        if diff % 11 == 0:
            result += perm_repeated[repeated] ** 2
    answer = result * 9 // 10
    print(answer)

if __name__ == "__main__":
    main()