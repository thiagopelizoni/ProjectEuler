# Problem: https://projecteuler.net/problem=458
def matrix_mult(A, B, mod):
    size = len(A)
    C = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(mat, exp, mod):
    size = len(mat)
    result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, mat, mod)
        mat = matrix_mult(mat, mat, mod)
        exp //= 2
    return result

def main():
    MOD = 1000000000
    n = 10**12
    size = 8
    M = [[0] * size for _ in range(size)]
    M[0][1] = 7
    for k in range(1, 7):
        for d in range(1, k + 1):
            M[k][d] = 1
        next_state = k + 1 if k < 6 else 7
        M[k][next_state] = 7 - k
    M[7][7] = 7
    powered = matrix_pow(M, n, MOD)
    all_strings = powered[7][7]
    with_project = powered[0][7]
    t = (all_strings - with_project + MOD) % MOD
    print(t)

if __name__ == "__main__":
    main()