# Problem: https://projecteuler.net/problem=382
def mat_mul(A, B, m):
    r = len(A)
    c = len(B[0])
    k = len(B)
    res = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            for p in range(k):
                res[i][j] = (res[i][j] + A[i][p] * B[p][j]) % m
    return res

def mat_pow(M, exp, m):
    size = len(M)
    res = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    while exp > 0:
        if exp % 2 == 1:
            res = mat_mul(res, M, m)
        M = mat_mul(M, M, m)
        exp //= 2
    return res

def mat_vec_mul(A, v, m):
    r = len(A)
    res = [0] * r
    for i in range(r):
        for j in range(len(v)):
            res[i] = (res[i] + A[i][j] * v[j]) % m
    return res

def main():

    mod = 1000000000
    n = 10**18
    exp = n - 9
    size = 9
    coeff = [3, -2, 2, -5, 1, 1, 3, -2]
    M = [[0] * size for _ in range(size)]
    M[0][0] = 1
    for i in range(8):
        M[0][i + 1] = coeff[i] % mod
    for i in range(8):
        M[1][i + 1] = coeff[i] % mod
    for i in range(1, size - 1):
        M[i + 1][i] = 1
    V = [272, 128, 67, 36, 20, 11, 6, 4, 2]
    Mp = mat_pow(M, exp, mod)
    Vf = mat_vec_mul(Mp, V, mod)
    S = Vf[0]
    pow2 = pow(2, n, mod)
    ans = (pow2 - 4 - S) % mod
    print(ans)

if __name__ == "__main__":
    main()