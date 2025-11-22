# Problem: https://projecteuler.net/problem=331
from math import isqrt
import numpy as np
from numba import njit, int64
from tqdm import tqdm
import sys

@njit(int64(int64))
def my_isqrt(n):
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

@njit(int64(int64))
def odd_compute(N):
    if N == 0:
        return 0
    total_black = int64(0)
    all_same = True
    first_par = int64(-1)
    max_s = int64(-1)
    j_max = int64(-1)
    bb = (N - 1) ** 2
    aa = N * N - 1
    v = my_isqrt(bb)
    u = my_isqrt(aa)
    k = int64(0)
    while k < N:
        lower = int64(0)
        if bb > 0:
            lower = v if v * v == bb else v + 1
        upper = min(u, N - 1)
        num = max(int64(0), upper - lower + 1)
        total_black += num
        par = num % 2
        if first_par == -1:
            first_par = par
        elif par != first_par:
            all_same = False
        if num > max_s:
            max_s = num
            j_max = k
        if k < N - 1:
            delta = 2 * k + 1
            bb -= delta
            aa -= delta
            while v * v > bb and v > 0:
                v -= 1
            while u * u > aa and u > 0:
                u -= 1
        k += 1
    if not all_same:
        return 0
    S = first_par
    if S == 0:
        return total_black
    else:
        jj_sq = 2 * j_max * j_max
        b_jj = 1 if (N - 1) ** 2 <= jj_sq < N * N else 0
        return total_black + 2 * N - 4 * max_s - 2 + 4 * b_jj

@njit(int64(int64))
def even_compute(N):
    parities = np.zeros(N, dtype=np.uint8)
    total_black = int64(0)
    bb = (N - 1) ** 2
    aa = N * N - 1
    v = my_isqrt(bb)
    u = my_isqrt(aa)
    k = int64(0)
    while k < N:
        lower = int64(0)
        if bb > 0:
            lower = v if v * v == bb else v + 1
        upper = min(u, N - 1)
        num = max(int64(0), upper - lower + 1)
        total_black += num
        parities[k] = num % 2
        if k < N - 1:
            delta = 2 * k + 1
            bb -= delta
            aa -= delta
            while v * v > bb and v > 0:
                v -= 1
            while u * u > aa and u > 0:
                u -= 1
        k += 1
    P = np.sum(parities) % 2
    r = np.bitwise_xor(parities, P)
    num1 = int64(0)
    for i in range(N):
        num1 += r[i]
    num0 = N - num1
    base = total_black + 2 * num0 * num1
    diff_black = int64(0)
    bb = (N - 1) ** 2
    aa = N * N - 1
    v = my_isqrt(bb)
    u = my_isqrt(aa)
    k = int64(0)
    while k < N:
        lower = int64(0)
        if bb > 0:
            lower = v if v * v == bb else v + 1
        upper = min(u, N - 1)
        r_k = r[k]
        for y in range(lower, upper + 1):
            if r_k != r[y]:
                diff_black += 1
        if k < N - 1:
            delta = 2 * k + 1
            bb -= delta
            aa -= delta
            while v * v > bb and v > 0:
                v -= 1
            while u * u > aa and u > 0:
                u -= 1
        k += 1
    return base - 2 * diff_black

def compute_T(N: int) -> int:
    N64 = int64(N)
    if N % 2 == 1:
        return odd_compute(N64)
    else:
        return even_compute(N64)

def main() -> None:
    total = 0
    for i in tqdm(range(3, 32), desc="Computing sum", file=sys.stderr):
        N = (1 << i) - i
        t = compute_T(N)
        total += t
    print(total)

if __name__ == "__main__":
    main()