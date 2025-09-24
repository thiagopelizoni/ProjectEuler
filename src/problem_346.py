# Problem: https://projecteuler.net/problem=346
import math
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Computes and prints the sum of all strong repunits below 10^12.

    Method / Math Rationale
    ------------------------
    Strong repunits are positive integers that are repunits in at least two
    different bases greater than 1. This includes 1 (repunit in all bases with
    one digit) and all numbers that are repunits with three or more digits in
    at least one base (since all numbers >=3 are repunits with two digits in
    base n-1). The algorithm generates all repunits with length >=3 by
    iteratively building the geometric series for each base starting from 2,
    adding unique values below the limit to the sum.

    Complexity
    ----------
    The outer loop runs up to approximately 10^6 bases, with inner loops
    averaging O(1) for large bases and up to O(log limit) for small bases,
    resulting in overall time complexity O(sqrt(limit) log limit) ≈ O(10^6).

    References
    ----------
    https://projecteuler.net/problem=346
    """
    limit = 10**12
    repunits = set()
    result = 1
    d = 4 * limit - 3
    max_b_float = (-1 + math.sqrt(d)) / 2
    max_base = int(max_b_float)
    for base in tqdm(range(2, max_base + 1)):
        n = 1 + base
        exp = 2
        while True:
            to_add = base ** exp
            n += to_add
            if n >= limit:
                break
            if n not in repunits:
                repunits.add(n)
                result += n
            exp += 1
    print(result)

if __name__ == "__main__":
    main()