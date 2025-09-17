# Problem: https://projecteuler.net/problem=324
import numpy as np
from collections import defaultdict, deque

def main():
    """
    Purpose:
    Computes f(10**10000) mod 100000007, where f(n) is the number of distinct ways
    to fill a 3x3xn tower with 2x1x1 blocks, allowing block rotations but counting
    tower symmetries as distinct.

    Method / Math Rationale:
    Models the problem using DP with bitmask states (0-511) representing protruding
    blocks in the 3x3 cross-section. Builds a 512x512 transfer matrix M where
    M[i][j] is the number of ways to tile one layer from incoming mask i to
    outgoing mask j. Reduces to 252 reachable states from mask 0. Computes T = M**2
    mod q, then reduces T to a 126x126 submatrix induced by states reachable from 0
    in T's transition graph. Since n is even, f(n) = (sub_T)**(n//2) [0, 0] mod q,
    computed via binary matrix exponentiation with modular multiplication.

    Complexity:
    O(s**3 * log n) time with s=126, log n ≈ 33220 (negligible preprocessing).

    References:
    https://projecteuler.net/problem=324
    """
    q = 100000007
    N = 9
    ALL = (1 << N) - 1
    partners = [
        [1, 3], [2, 4], [5], [4, 6], [5, 7], [8], [7], [8], []
    ]

    def build_transitions():
        M = [[0] * 512 for _ in range(512)]
        for mask_in in range(512):
            count = defaultdict(int)
            def backtrack(pos, remaining, out):
                if pos == 9:
                    if remaining == 0:
                        count[out] += 1
                    return
                if (remaining & (1 << pos)) == 0:
                    backtrack(pos + 1, remaining, out)
                    return
                new_rem = remaining ^ (1 << pos)
                new_out = out | (1 << pos)
                backtrack(pos + 1, new_rem, new_out)
                for p in partners[pos]:
                    if (remaining & (1 << p)) != 0:
                        new_rem = remaining ^ (1 << pos) ^ (1 << p)
                        backtrack(pos + 1, new_rem, out)
            initial_rem = (~mask_in & ALL)
            backtrack(0, initial_rem, 0)
            for out, ways in count.items():
                M[mask_in][out] = ways % q
        return M

    M = build_transitions()

    reachable = set()
    queue = deque([0])
    reachable.add(0)
    while queue:
        current = queue.popleft()
        for next_state in range(512):
            if M[current][next_state] > 0 and next_state not in reachable:
                reachable.add(next_state)
                queue.append(next_state)

    state_list = sorted(reachable)
    k = len(state_list)
    state_id = {state_list[i]: i for i in range(k)}

    small_M = np.zeros((k, k), dtype=np.int64)
    for i in range(k):
        old_i = state_list[i]
        for old_j in range(512):
            w = M[old_i][old_j]
            if w > 0 and old_j in state_id:
                j = state_id[old_j]
                small_M[i, j] = w

    T = np.dot(small_M, small_M) % q

    reach2 = set()
    queue = deque([0])
    reach2.add(0)
    while queue:
        current = queue.popleft()
        for next_state in range(k):
            if T[current, next_state] > 0 and next_state not in reach2:
                reach2.add(next_state)
                queue.append(next_state)

    sub_list = sorted(reach2)
    l = len(sub_list)
    sub_T = np.zeros((l, l), dtype=np.int64)
    for i in range(l):
        for j in range(l):
            sub_T[i, j] = T[sub_list[i], sub_list[j]]

    def mat_pow(mat, exp, mod):
        n = mat.shape[0]
        result = np.eye(n, dtype=np.int64)
        while exp > 0:
            if exp % 2 == 1:
                result = np.dot(result, mat) % mod
            mat = np.dot(mat, mat) % mod
            exp //= 2
        return result

    n = 10 ** 10000
    m = n // 2
    powered = mat_pow(sub_T, m, q)
    print(powered[0, 0])

if __name__ == "__main__":
    main()