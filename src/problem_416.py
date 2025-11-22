# Problem: https://projecteuler.net/problem=416
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from math import factorial
from collections import defaultdict
from tqdm import tqdm
import numpy as np
from numba import jit

@jit(nopython=True)
def mat_mult(A, B, m):
    D = A.shape[0]
    res = np.zeros((D, D), dtype=np.int64)
    for i in range(D):
        for j in range(D):
            for k in range(D):
                res[i][j] += A[i][k] * B[k][j]
                res[i][j] %= m
    return res

@jit(nopython=True)
def mat_vec_mult(A, v, m):
    D = A.shape[0]
    res = np.zeros(D, dtype=np.int64)
    for i in range(D):
        for k in range(D):
            res[i] += A[i][k] * v[k]
        res[i] %= m
    return res

@jit(nopython=True)
def mat_pow_with_der(P_base, D_base, exp, m, D):
    P = np.eye(D, dtype=np.int64) % m
    D_der = np.zeros((D, D), dtype=np.int64) % m
    while exp > 0:
        if exp % 2 == 1:
            D_new = (mat_mult(D_der, P_base, m) + mat_mult(P, D_base, m)) % m
            P = mat_mult(P, P_base, m) % m
            D_der = D_new
        D_base_new = (mat_mult(D_base, P_base, m) + mat_mult(P_base, D_base, m)) % m
        P_base = mat_mult(P_base, P_base, m) % m
        D_base = D_base_new
        exp //= 2
    return P, D_der

def build_rep(M, D, mon, id_dict, m):
    T = np.zeros((D, D), dtype=np.int64)
    row0 = M[0]
    row1 = M[1]
    row2 = M[2]
    for j in range(D):
        a, b, c = mon[j]
        poly_a = power_poly(row0, a)
        poly_b = power_poly(row1, b)
        poly_c = power_poly(row2, c)
        poly = multiply_poly(poly_a, poly_b)
        poly = multiply_poly(poly, poly_c)
        for key, coef in poly.items():
            i = id_dict.get(key)
            if i is not None:
                T[i][j] = (T[i][j] + coef) % m
    return T

def power_poly(p, exp):
    if exp == 0:
        return {(0, 0, 0): 1}
    poly = defaultdict(int)
    for i in range(exp + 1):
        for j in range(exp - i + 1):
            k = exp - i - j
            mult = factorial(exp) // (factorial(i) * factorial(j) * factorial(k))
            coef = mult * p[0]**i * p[1]**j * p[2]**k
            poly[(i, j, k)] = coef
    return poly

def multiply_poly(p1, p2):
    new_poly = defaultdict(int)
    for k1, c1 in p1.items():
        for k2, c2 in p2.items():
            new_k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            new_poly[new_k] += c1 * c2
    return new_poly

def compute_mod(m, n):
    DEG = 20
    D = int((DEG + 1) * (DEG + 2) / 2)
    mon = []
    id_dict = {}
    idx = 0
    for a in range(DEG + 1):
        for b in range(DEG - a + 1):
            c = DEG - a - b
            mon.append((a, b, c))
            id_dict[(a, b, c)] = idx
            idx += 1
    Ma = np.array([[1, 1, 1], [1, 0, 0], [0, 1, 0]], dtype=np.int64)
    Mr = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.int64)
    A = build_rep(Ma, D, mon, id_dict, m)
    B = build_rep(Mr, D, mon, id_dict, m)
    P_base = (A - B + m) % m
    D_base = B % m
    P, D_der = mat_pow_with_der(P_base, D_base, n - 2, m, D)
    initial_poly = power_poly(Ma[0], DEG)
    initial_v = np.zeros(D, dtype=np.int64)
    for key, coef in initial_poly.items():
        i = id_dict.get(key)
        if i is not None:
            initial_v[i] = coef % m
    p_v = mat_vec_mult(P, initial_v, m)
    d_v = mat_vec_mult(D_der, initial_v, m)
    index20 = id_dict[(DEG, 0, 0)]
    S0 = p_v[index20]
    S1 = (-d_v[index20]) % m
    return (S0 - S1) % m

def chinese_remainder(a1, m1, a2, m2):
    inv = pow(m1, -1, m2)
    k = ((a2 - a1) % m2 * inv) % m2
    x = (a1 + m1 * k) % (m1 * m2)
    return x

def main():
    n = 10**12
    MOD = 10**9
    m1 = 512
    m2 = 1953125
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(compute_mod, m1, n), executor.submit(compute_mod, m2, n)]
        for future in tqdm(futures):
            future.result()
        f1 = futures[0].result()
        f2 = futures[1].result()
    ans = chinese_remainder(f1, m1, f2, m2)
    print(ans)

if __name__ == "__main__":
    main()