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
    """
    Purpose
    -------
    Compute the sums S(n) = sum_{k=1}^n floor(k * phi), U(n) = sum_{k=1}^n k * floor(k * phi),
    V(n) = sum_{k=1}^n floor(k * phi)^2 where phi = (1 + sqrt(5))/2.

    Args
    ----
    None

    Returns
    -------
    None

    Method / Math Rationale
    -----------------------
    Uses recursive Beatty partition of natural numbers into Wythoff sequences A and B.
    S(n) = N(N+1)/2 - S(J) - J(J+1)/2
    V(n) = N(N+1)(2N+1)/6 - V(J) - 2 U(J) - J(J+1)(2J+1)/6
    U(n) = [n(n+1)/2] * (n + J) - [n(n+1)(n-1)/3 + V(J) + S(J)] / 2
    where N = floor(n * phi), J = N - n.
    Floor computed via binary search for floor(n * sqrt(5)).

    Complexity
    ----------
    O(log n)

    References
    ----------
    https://projecteuler.net/problem=325
    """
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
    """
    Purpose
    -------
    Solve Project Euler problem 325: compute S(10^16) mod 7^10, where S(N) is the sum of x+y over
    losing positions (x,y) with 0 < x < y <= N in the stone game.

    Method / Math Rationale
    -----------------------
    Losing positions are those with y <= floor(x * phi) where phi = (1 + sqrt(5))/2.
    Split sum at K = floor(N / phi). For x = 1 to K, use sums S(K), U(K), V(K) over
    floor(k * phi) combined as [2*U(K) + V(K) + S(K) - sum x - 3*sum x^2] // 2.
    For x = K+1 to N-1, closed-form sum_d=1^{N-K-1} d*(4*N - 3*d + 1)//2.
    S, U, V computed recursively using Beatty partition.

    Complexity
    ----------
    O(log N)

    References
    ----------
    https://projecteuler.net/problem=325
    """
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