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