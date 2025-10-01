# Problem: https://projecteuler.net/problem=376
import numpy as np
from numba import njit
from tqdm import tqdm

@njit
def update(current, next_state):
    R = 7
    W = 37
    for ra in range(R):
        for rb in range(R):
            for rc in range(R):
                cum_b = 6 - rb
                cum_c = 6 - rc
                cum_a = 6 - ra
                for wab in range(W):
                    for wbc in range(W):
                        for wca in range(W):
                            cnt = current[ra, rb, rc, wab, wbc, wca]
                            if cnt == 0:
                                continue
                            for fa in range(ra + 1):
                                add_ab = fa * cum_b
                                new_wab = wab + add_ab
                                if new_wab >= W:
                                    continue
                                new_ra = ra - fa
                                for fb in range(rb + 1):
                                    add_bc = fb * cum_c
                                    new_wbc = wbc + add_bc
                                    if new_wbc >= W:
                                        continue
                                    new_rb = rb - fb
                                    for fc in range(rc + 1):
                                        add_ca = fc * cum_a
                                        new_wca = wca + add_ca
                                        if new_wca >= W:
                                            continue
                                        new_rc = rc - fc
                                        next_state[new_ra, new_rb, new_rc, new_wab, new_wbc, new_wca] += cnt

@njit
def get_total(current):
    total = np.uint64(0)
    for wab in range(19, 37):
        for wbc in range(19, 37):
            for wca in range(19, 37):
                total += current[0, 0, 0, wab, wbc, wca]
    return total

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 376 by counting the number of distinct unordered sets of three six-sided dice
    with faces numbered from 1 to 30 that form a nontransitive set, where for any die chosen first, the second
    player can choose another with >1/2 probability of winning.

    Method / Math Rationale
    ------------------------
    Uses dynamic programming over the pip values from 1 to N=30, tracking the remaining faces to assign for each
    die (A, B, C) and the cumulative strict win counts for A over B, B over C, C over A. At each pip value,
    assigns counts to each die and updates win counts based on prefix cumulatives. At the end, sums the ways
    where all win counts >18 (corresponding to >1/2 probability), dividing by 3 for unordered sets. The
    conditions ensure distinct dice.

    Complexity
    ----------
    O(N * 7^3 * 37^3 * 7^3) in the worst case due to state space and transitions, but accelerated with Numba JIT
    compilation for performance.

    References
    ----------
    https://projecteuler.net/problem=376
    """
    N = 30
    R = 7
    W = 37
    current = np.zeros((R, R, R, W, W, W), dtype=np.uint64)
    current[6, 6, 6, 0, 0, 0] = 1
    for _ in tqdm(range(N)):
        next_state = np.zeros((R, R, R, W, W, W), dtype=np.uint64)
        update(current, next_state)
        current = next_state
    total = get_total(current)
    print(total // 3)

if __name__ == "__main__":
    main()