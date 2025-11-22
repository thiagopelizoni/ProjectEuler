# Problem: https://projecteuler.net/problem=325
from typing import Tuple

def floor_sqrt5_times_n(n: int) -> int:
    if n == 0:
        return 0
    low = 0
    high = 3 * n
    while low < high:
        mid = low + (high - low + 1) // 2
        if mid * mid <= 5 * n * n:
            low = mid
        else:
            high = mid - 1
    return low

def floor_phi(n: int) -> int:
    return (n + floor_sqrt5_times_n(n)) // 2

memo: dict[int, Tuple[int, int, int]] = {}

def get_suv(n: int) -> Tuple[int, int, int]:
    if n <= 0:
        return 0, 0, 0
    if n in memo:
        return memo[n]
    N = floor_phi(n)
    J = N - n
    sj, uj, vj = get_suv(J)
    s = N * (N + 1) // 2 - sj - J * (J + 1) // 2
    v = N * (N + 1) * (2 * N + 1) // 6 - vj - 2 * uj - J * (J + 1) * (2 * J + 1) // 6
    an = n + J
    temp = n * (n + 1) * (n - 1) // 3 + vj + sj
    u = n * (n + 1) // 2 * an - temp // 2
    memo[n] = s, u, v
    return s, u, v

def main() -> None:
    N = 10**16
    mod = 7**10
    A = floor_phi(N) - N
    sm, um, vm = get_suv(A)
    sumx = A * (A + 1) // 2
    sumx2 = A * (A + 1) * (2 * A + 1) // 6
    first = (2 * um + vm + sm - sumx - 3 * sumx2) // 2
    if A + 1 > N - 1:
        second = 0
    else:
        D = N - A - 1
        sumd = D * (D + 1) // 2
        sumd2 = D * (D + 1) * (2 * D + 1) // 6
        temp = (4 * N + 1) * sumd - 3 * sumd2
        second = temp // 2
    total = (first + second) % mod
    print(total)

if __name__ == "__main__":
    main()