# Problem: https://projecteuler.net/problem=411
import bisect
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def longest_nondec_subseq(ys):
    if not ys:
        return 0
    active = []
    for num in ys:
        if not active or num >= active[-1]:
            active.append(num)
        else:
            idx = bisect.bisect_right(active, num)
            active[idx] = num
    return len(active)

def compute_S(k):
    n = k ** 5
    S = set()
    x = 1 % n
    y = 1 % n
    for _ in tqdm(range(2 * n + 1), desc=f"Generating for k={k}", leave=False):
        S.add((x, y))
        x = (x * 2) % n
        y = (y * 3) % n
    points = sorted(S)
    ys = [p[1] for p in points]
    return longest_nondec_subseq(ys)

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 411 by computing the sum of S(k^5) for k=1 to 30.

    Method / Math Rationale
    -----------------------
    For each n = k^5, generate distinct stations by iteratively computing
    x = (x*2) % n, y = (y*3) % n for up to 2n+1 steps, using a set for uniqueness. Sort the
    points by x then y. Compute the longest non-decreasing subsequence length on the
    y-coordinates using a modified patience sorting algorithm with bisect_right for
    non-strict inequality. This gives S(n) as the longest chain in the poset. Use
    parallelism across k values for performance.

    Complexity
    ----------
    O(sum_{k=1 to 30} (2 * k^5 + m log m)) where m is the number of distinct stations for
    each n, with m << k^5 in practice.

    References
    ----------
    https://projecteuler.net/problem=411
    """
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_S, range(1, 31)))
    print(sum(results))

if __name__ == "__main__":
    main()