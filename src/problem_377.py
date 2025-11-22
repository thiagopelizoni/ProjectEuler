# Problem: https://projecteuler.net/problem=377
from tqdm import tqdm

def mat_mul(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C


def mat_pow(mat, exp, mod):
    n = len(mat)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while exp > 0:
        if exp % 2 == 1:
            result = mat_mul(result, mat, mod)
        mat = mat_mul(mat, mat, mod)
        exp //= 2
    return result


def vec_mul(mat, vec, mod):
    n = len(vec)
    new_vec = [0] * n
    for i in range(n):
        for j in range(n):
            new_vec[i] = (new_vec[i] + mat[i][j] * vec[j]) % mod
    return new_vec


def compute_f(n, mod, M, initial_state):
    exp = n - 8
    powered = mat_pow(M, exp, mod)
    new_state = vec_mul(powered, initial_state, mod)
    return new_state[0]


def main():
    MOD = 1000000000
    size = 18

    M = [[0 for _ in range(size)] for _ in range(size)]
    for j in range(9):
        M[0][j] = 10
    for idx, val in enumerate(range(1, 10)):
        M[0][9 + idx] = val
    for row in range(1, 9):
        M[row][row - 1] = 1
    for j in range(9, 18):
        M[9][j] = 1
    for row in range(10, 18):
        M[row][row - 1] = 1

    initial_state = [
        23817625, 2165227, 196833, 17891, 1625, 147, 13, 1, 0,
        128, 64, 32, 16, 8, 4, 2, 1, 1
    ]

    powers = []
    cur = 13
    for _ in range(17):
        powers.append(cur)
        cur *= 13

    total = 0
    for p in tqdm(powers):
        total = (total + compute_f(p, MOD, M, initial_state)) % MOD

    print(total)


if __name__ == "__main__":
    main()