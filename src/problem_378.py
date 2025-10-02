# Problem: https://projecteuler.net/problem=378

import numpy as np
from tqdm import tqdm
import numba as nb


@nb.jit(nopython=True)
def ft_update(tree, index, val, size):
    while index <= size:
        tree[index] += val
        index += index & -index


@nb.jit(nopython=True)
def ft_query(tree, index):
    s = 0
    while index > 0:
        s += tree[index]
        index -= index & -index
    return s


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 378 by computing Tr(60000000) and printing
    its last 18 digits.

    Method / Math Rationale
    ------------------------
    Precompute number of divisors for all numbers up to N+1 using a
    sieve-like method. Then compute dT(k) for each k using the formula
    based on parity of k. Then use two Fenwick trees to efficiently count
    the number of decreasing triples in the sequence dT[1..N]. One tree
    tracks the count of each dT value, the other tracks the sum of prefix
    higher counts for each value.

    Complexity
    ----------
    O(N log N) for divisor precomputation, O(N) for dT computation,
    O(N log D) for the triple counting, where D is the maximum dT value
    (around 10^4).

    References
    ----------
    https://projecteuler.net/problem=378
    """
    N = 60000000

    d = np.zeros(N + 2, dtype=np.int32)
    for i in tqdm(range(1, N + 2)):
        d[i::i] += 1

    dT = np.zeros(N + 1, dtype=np.int32)
    for k in range(1, N + 1):
        if k % 2 == 0:
            dT[k] = d[k // 2] * d[k + 1]
        else:
            dT[k] = d[k] * d[(k + 1) // 2]

    max_d = int(dT.max())
    D = max_d + 1

    FT_count_tree = np.zeros(D + 1, dtype=np.int64)
    FT_sum_tree = np.zeros(D + 1, dtype=np.int64)

    total = 0
    for k in tqdm(range(1, N + 1)):
        v = int(dT[k])
        contrib = ft_query(FT_sum_tree, D) - ft_query(FT_sum_tree, v)
        total += contrib

        left_higher = ft_query(FT_count_tree, D) - ft_query(FT_count_tree, v)
        ft_update(FT_sum_tree, v, left_higher, D)
        ft_update(FT_count_tree, v, 1, D)

    print(total % 1000000000000000000)

if __name__ == "__main__":
    main()