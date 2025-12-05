# Problem: https://projecteuler.net/problem=546
import numpy as np
from numba import njit, prange, int64

MOD = 10**9 + 7
TARGET_N = 10**14
MIN_K = 2
MAX_K = 10
MATRIX_SIZE = 60
TABLE_SIZE = 1500 

@njit(fastmath=True, cache=True)
def mod_pow(base, exp):
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

@njit(fastmath=True, cache=True)
def mod_inv(a):
    return mod_pow(a, MOD - 2)

@njit(fastmath=True, cache=True)
def mat_mul_mod(A, B):
    rows_A = A.shape[0]
    cols_A = A.shape[1]
    cols_B = B.shape[1]
    C = np.zeros((rows_A, cols_B), dtype=np.int64)
    for i in range(rows_A):
        for k in range(cols_A):
            if A[i, k] == 0: continue
            val_a = A[i, k]
            for j in range(cols_B):
                C[i, j] = (C[i, j] + val_a * B[k, j]) % MOD
    return C

@njit(fastmath=True, cache=True)
def mat_vec_mul_mod(A, v):
    size = A.shape[0]
    res = np.zeros(size, dtype=np.int64)
    for i in range(size):
        acc = 0
        for j in range(size):
            acc = (acc + A[i, j] * v[j]) % MOD
        res[i] = acc
    return res

@njit(fastmath=True, cache=True)
def mat_inv_mod(M):
    n = M.shape[0]
    A = M.copy().astype(np.int64)
    I = np.eye(n, dtype=np.int64)
    for i in range(n):
        pivot = A[i, i]
        if pivot == 0:
            for j in range(i + 1, n):
                if A[j, i] != 0:
                    tmp_row_A = A[i].copy(); A[i] = A[j]; A[j] = tmp_row_A
                    tmp_row_I = I[i].copy(); I[i] = I[j]; I[j] = tmp_row_I
                    pivot = A[i, i]
                    break
        inv_pivot = mod_inv(pivot)
        for k in range(n):
            A[i, k] = (A[i, k] * inv_pivot) % MOD
            I[i, k] = (I[i, k] * inv_pivot) % MOD
        for j in range(n):
            if i != j:
                factor = A[j, i]
                if factor != 0:
                    for k in range(n):
                        A[j, k] = (A[j, k] - factor * A[i, k]) % MOD
                        I[j, k] = (I[j, k] - factor * I[i, k]) % MOD
    for i in range(n):
        for j in range(n):
            if I[i, j] < 0:
                I[i, j] += MOD
    return I

@njit(fastmath=True, cache=True)
def compute_s_table(k, size, max_depth):
    s_table = np.zeros((max_depth, size), dtype=np.int64)
    s_table[0, 0] = 1
    for n in range(1, size):
        term = s_table[0, n // k]
        s_table[0, n] = (s_table[0, n-1] + term) % MOD
    for d in range(1, max_depth):
        current_sum = 0
        for n in range(size):
            current_sum = (current_sum + s_table[d-1, n]) % MOD
            s_table[d, n] = current_sum
    return s_table

@njit(fastmath=True, cache=True)
def solve_for_k(k):
    s_table = compute_s_table(k, TABLE_SIZE, MATRIX_SIZE)
    V_curr = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=np.int64)
    for c in range(MATRIX_SIZE): 
        n = c 
        for r in range(MATRIX_SIZE): 
            V_curr[r, c] = s_table[r, n]
    V_curr_inv = mat_inv_mod(V_curr)
    matrices = np.zeros((k, MATRIX_SIZE, MATRIX_SIZE), dtype=np.int64)
    for r_digit in range(k):
        V_next = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=np.int64)
        for c in range(MATRIX_SIZE): 
            n = c
            target_idx = n * k + r_digit
            for row in range(MATRIX_SIZE): 
                V_next[row, c] = s_table[row, target_idx]
        M = mat_mul_mod(V_next, V_curr_inv)
        matrices[r_digit] = M
    temp_n = TARGET_N
    digits = []
    while temp_n > 0:
        digits.append(temp_n % k)
        temp_n //= k
    state = np.zeros(MATRIX_SIZE, dtype=np.int64)
    for i in range(MATRIX_SIZE):
        state[i] = 1 
    for i in range(len(digits) - 1, -1, -1):
        digit = digits[i]
        M = matrices[digit]
        state = mat_vec_mul_mod(M, state)
    return state[0]

@njit(parallel=True, fastmath=True, cache=True)
def main_parallel():
    total_sum = 0
    for k in prange(MIN_K, MAX_K + 1):
        val = solve_for_k(k)
        total_sum += val
    return total_sum % MOD

def main():
    result = main_parallel()
    print(result)

if __name__ == "__main__":
    main()