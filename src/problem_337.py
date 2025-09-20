# Problem: https://projecteuler.net/problem=337
import numpy as np
from numba import njit
from tqdm import tqdm

@njit
def ft_update(tree, index: int, value: float, size: int):
    while index <= size:
        tree[index] += value
        index += index & -index

@njit
def ft_query(tree, index: int) -> float:
    s = 0.0
    while index > 0:
        s += tree[index]
        index -= index & -index
    return s

def compute_phi(n: int) -> np.ndarray:
    phi = np.arange(n + 1, dtype=np.int32)
    for i in range(2, n + 1):
        if phi[i] == i:
            for j in range(i, n + 1, i):
                phi[j] = phi[j] // i * (i - 1)
    return phi

def main():
    """
    Purpose
    Compute S(20,000,000) mod 10^8, where S(N) is the number of totient stairstep sequences with a_n <= N.

    Args
    None

    Returns
    None

    Method / Math Rationale
    Precompute Euler's totient function for all numbers up to N using a sieve.
    Use dynamic programming: dp[m] = sum of dp[k] over valid predecessors k, plus 1 if m=6.
    To efficiently compute the sums, process numbers in order of increasing phi[m], grouping by phi value to handle
    equal phi correctly.
    Use a Fenwick tree (binary indexed tree) for range sum queries and updates to accumulate the dp values modulo 10^8.

    Complexity
    Time: O(N log N) due to sorting and Fenwick tree operations.
    Space: O(N)

    References
    https://projecteuler.net/problem=337
    """
    N = 20000000
    MOD = 100000000
    phi = compute_phi(N)
    items = [(phi[m], m) for m in range(6, N + 1)]
    items.sort()
    tree = np.zeros(N + 1, dtype=np.float64)
    total = 0
    current_p = -1
    pending_updates = []
    for item in tqdm(items):
        p, m = item
        if p != current_p:
            for pm, pval in pending_updates:
                ft_update(tree, pm, pval, N)
            pending_updates = []
            current_p = p
        left = p + 1
        right = m - 1
        query_val = 0.0
        if left <= right:
            query_val = ft_query(tree, right) - ft_query(tree, left - 1)
        add = 1 if m == 6 else 0
        val = query_val + add
        val_mod = int(val) % MOD
        total = (total + val_mod) % MOD
        pending_updates.append((m, val_mod))
    for pm, pval in pending_updates:
        ft_update(tree, pm, pval, N)
    print(total)

if __name__ == "__main__":
    main()