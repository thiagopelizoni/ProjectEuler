# Problem: https://projecteuler.net/problem=356
from tqdm import tqdm

def matrix_multiply(A, B, mod):
    """
    Multiply two 3x3 matrices modulo mod.
    """
    rows = len(A)
    C = [[0] * rows for _ in range(rows)]
    for i in range(rows):
        for j in range(rows):
            for l in range(rows):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % mod
    return C

def matrix_power(mat, exp, mod):
    """
    Compute matrix to the power exp modulo mod using exponentiation by squaring.
    """
    rows = len(mat)
    result = [[1 if i == j else 0 for j in range(rows)] for i in range(rows)]
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_multiply(result, mat, mod)
        mat = matrix_multiply(mat, mat, mod)
        exp //= 2
    return result

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 356 by computing the last eight digits of the sum from i=1 to 30
    of floor(a_i^{987654321}), where a_i is the largest real root of x^3 - 2^i x^2 + i = 0.
    
    Method / Math Rationale
    -----------------------
    For each n, define v_k = alpha^k + beta^k + gamma^k, where alpha, beta, gamma are the roots,
    with alpha the largest. v_k is an integer satisfying the recurrence v_m = 2^n v_{m-1} - n v_{m-3}.
    Since k is odd and beta > |gamma| > 0 with gamma < 0, beta^k + gamma^k > 0. Thus,
    floor(alpha^k) = v_k - 1. Compute v_k mod 10^8 using modular matrix exponentiation for each n,
    sum them, subtract 30, and take mod 10^8 to get the last eight digits.
    
    Complexity
    ----------
    O(30 * log(k) * 27) where k=987654321, effectively constant time.
    
    References
    ----------
    https://projecteuler.net/problem=356
    """
    mod = 100000000
    k = 987654321
    total = 0
    
    for n in tqdm(range(1, 31)):
        pow2n = 1 << n
        pow4n = 1 << (2 * n)
        M = [[pow2n % mod, 0, (mod - n) % mod],
             [1, 0, 0],
             [0, 1, 0]]
        initial_vec = [pow4n % mod, pow2n % mod, 3 % mod]
        
        if k == 2:
            v_k = initial_vec[0]
        else:
            powered = matrix_power(M, k - 2, mod)
            v_k = 0
            for j in range(3):
                v_k = (v_k + powered[0][j] * initial_vec[j]) % mod
        
        total = (total + v_k) % mod
    
    result = (total - 30) % mod
    print(result)

if __name__ == "__main__":
    main()