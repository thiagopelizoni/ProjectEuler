# Problem: https://projecteuler.net/problem=461
import math
from bisect import bisect_right
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 461 by finding non-negative integers a, b, c, d
    that minimize the absolute error |f_n(a) + f_n(b) + f_n(c) + f_n(d) - pi|,
    where f_n(k) = exp(k/n) - 1 and n=10000, then compute and print
    g(n) = a^2 + b^2 + c^2 + d^2.

    Method / Math Rationale
    -----------------------
    Precompute f[k] = exp(k/n) - 1 for k from 0 until f[k] > pi.
    Generate pair sums s = f[i] + f[j] for i <= j, s <= pi.
    Sort the pair sums.
    For each potential left pair sum current, compute need = pi - current.
    Use binary search to find the right pair sum closest to need.
    Track the left and right indices with the minimal error.
    Resolve a, b and c, d by re-computing pairs until matching the sums.
    The method uses meet-in-the-middle on pairs to reduce complexity.
    Math: the sum of four f terms approximates pi closely for optimal choices.

    Complexity
    ----------
    Time: O(M^2 log M) for sorting pairs, where M ~ 1.42 * n ~ 14200,
    pair generation O(M^2), loop over pairs O(P) with P ~ 7e7, each O(1).
    Resolving: worst O(M^2) per, but practical as loops break early.
    Space: O(P) for pairs ~ 576 MB.

    References
    ----------
    https://projecteuler.net/problem=461
    """
    n = 10000
    pi = math.pi
    f = []
    k = 0
    while True:
        current = math.exp(k / n) - 1
        if current > pi:
            break
        f.append(current)
        k += 1
    maximum = len(f)
    pairs = []
    for i in tqdm(range(maximum)):
        for j in range(i, maximum):
            s = f[i] + f[j]
            if s > pi:
                break
            pairs.append(s)
    pairs.sort()
    min_error = pi
    left = 0
    right = 0
    for idx in range(len(pairs)):
        current = pairs[idx]
        need = pi - current
        if need < current:
            break
        pos = bisect_right(pairs, need)
        for p in [pos, pos - 1]:
            if 0 <= p < len(pairs):
                error = abs(need - pairs[p])
                if error < min_error:
                    min_error = error
                    left = idx
                    right = p
    # resolve left
    sum_left = pairs[left]
    a = b = None
    for i in range(maximum):
        for j in range(i, maximum):
            if abs(f[i] + f[j] - sum_left) < 1e-12:
                a = i
                b = j
                goto_next = True
                break
        if a is not None:
            break
    # resolve right
    sum_right = pairs[right]
    c = d = None
    for i in range(maximum):
        for j in range(i, maximum):
            if abs(f[i] + f[j] - sum_right) < 1e-12:
                c = i
                d = j
                break
        if c is not None:
            break
    g = a**2 + b**2 + c**2 + d**2
    print(g)

if __name__ == "__main__":
    main()