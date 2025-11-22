# Problem: https://projecteuler.net/problem=270
# Problem: https://projecteuler.net/problem=270

from tqdm import tqdm
from typing import List, Set, Tuple

def main() -> None:
    N: int = 30
    V: int = 4 * N
    MOD: int = 10**8

    sides: List[Set[str]] = [set() for _ in range(V)]
    pos: List[Tuple[int, int]] = [(0, 0) for _ in range(V)]

    for idx in range(V):
        if 0 <= idx <= N:
            pos[idx] = (idx, 0)
            if idx == 0:
                sides[idx] = {'b', 'l'}
            elif idx == N:
                sides[idx] = {'b', 'r'}
            else:
                sides[idx] = {'b'}
        elif N < idx <= 2 * N:
            pos[idx] = (N, idx - N)
            if idx == 2 * N:
                sides[idx] = {'r', 't'}
            else:
                sides[idx] = {'r'}
        elif 2 * N < idx <= 3 * N:
            pos[idx] = (N - (idx - 2 * N), N)
            if idx == 3 * N:
                sides[idx] = {'t', 'l'}
            else:
                sides[idx] = {'t'}
        else:
            pos[idx] = (0, N - (idx - 3 * N))
            sides[idx] = {'l'}

    dp: List[List[int]] = [[0] * V for _ in range(V)]
    for i in range(V - 1):
        dp[i][i + 1] = 1

    def is_allowed(a: int, b: int) -> bool:
        return not sides[a] & sides[b]

    def is_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) == 0

    for length in tqdm(range(2, V)):
        for i in range(V - length):
            j: int = i + length
            for k in range(i + 1, j):
                allowed_ik: bool = (k == i + 1) or is_allowed(i, k)
                allowed_kj: bool = (k == j - 1) or is_allowed(k, j)
                not_col: bool = not is_collinear(pos[i], pos[k], pos[j])
                if allowed_ik and allowed_kj and not_col:
                    dp[i][j] = (dp[i][j] + dp[i][k] * dp[k][j]) % MOD

    print(dp[0][V - 1])

if __name__ == "__main__":
    main()