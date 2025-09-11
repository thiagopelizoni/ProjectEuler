# Problem: https://projecteuler.net/problem=303
import concurrent.futures
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def compute_k(n):
    seen = set()
    queue = deque()
    parent = {}
    for start_d in [1, 2]:
        r = start_d % n
        if r not in seen:
            seen.add(r)
            queue.append(r)
            parent[r] = (-1, start_d)
            if r == 0:
                return start_d // n
    while queue:
        current_r = queue.popleft()
        for d in range(3):
            new_r = (current_r * 10 + d) % n
            if new_r == 0:
                digits = [str(d)]
                rem = current_r
                while rem != -1:
                    prev, dig = parent[rem]
                    digits.append(str(dig))
                    rem = prev
                m_str = ''.join(digits[::-1])
                m = int(m_str)
                return m // n
            if new_r not in seen:
                seen.add(new_r)
                queue.append(new_r)
                parent[new_r] = (current_r, d)

def main():
    """
    Purpose
    Solves Project Euler problem 303 by computing the sum of f(n)/n for n from 1 to 10000, where f(n) is the smallest
    positive multiple of n using only digits 0, 1, or 2.

    Method / Math Rationale
    For each n, use BFS on remainders modulo n to find the smallest number (in terms of length then lexicographical
    order) composed of digits 0-2 that is divisible by n. This is achieved by exploring digit additions while tracking
    remainders, stopping when remainder 0 is reached. The number is reconstructed from parent pointers, converted to
    int, and divided by n to get k = f(n)/n. Sum all k using parallel processing for efficiency.

    Complexity
    Time: O(N^2) where N=10000, since for each of 10000 n, BFS is O(n). Space: O(N) per BFS.

    References
    https://projecteuler.net/problem=303
    """
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_k, n) for n in range(1, 10001)]
    total = 0
    for future in tqdm(as_completed(futures), total=10000):
        total += future.result()
    print(total)

if __name__ == "__main__":
    main()