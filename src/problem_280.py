# Problem: https://projecteuler.net/problem=280
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def get_neighbors(r, c):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 1 <= nr <= 5 and 1 <= nc <= 5:
            neighbors.append((nr, nc))
    return neighbors

def main():
    rows = range(1, 6)
    cols = range(1, 6)
    all_possible_states = []
    for r in rows:
        for c in cols:
            for carry in [0, 1]:
                for tm in range(32):
                    for bm in range(32):
                        pc_t = bin(tm).count('1')
                        pc_b = bin(bm).count('1')
                        if pc_t + pc_b + carry == 5:
                            all_possible_states.append((r, c, carry, tm, bm))

    transient_states = [s for s in all_possible_states if not (s[4] == 0 and s[2] == 0)]
    N = len(transient_states)
    state_to_idx = {transient_states[i]: i for i in range(N)}

    A = lil_matrix((N, N))
    b = np.ones(N)
    for i in range(N):
        A[i, i] = 1.0

    for i in range(N):
        s = transient_states[i]
        r, c, carry, tm, bm = s
        neighbors = get_neighbors(r, c)
        prob = 1.0 / len(neighbors)
        for nr, nc in neighbors:
            next_carry = carry
            next_tm = tm
            next_bm = bm
            if nr == 5 and next_carry == 0 and (next_bm & (1 << (nc - 1))):
                next_carry = 1
                next_bm ^= (1 << (nc - 1))
            if nr == 1 and next_carry == 1 and not (next_tm & (1 << (nc - 1))):
                next_carry = 0
                next_tm |= (1 << (nc - 1))
            next_s = (nr, nc, next_carry, next_tm, next_bm)
            if next_s in state_to_idx:
                j = state_to_idx[next_s]
                A[i, j] -= prob

    A = A.tocsr()
    x = spsolve(A, b)

    initial_state = (3, 3, 0, 0, 31)
    initial_idx = state_to_idx[initial_state]
    ans = x[initial_idx]
    print(f"{ans:.6f}")

if __name__ == "__main__":
    main()