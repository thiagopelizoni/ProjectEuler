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
    """
    Purpose
    -------
    Solves Project Euler problem 458 by computing the last 9 digits of T(10^12),
    where T(n) is the number of strings of length n over a 7-letter alphabet
    that do not contain any substring of 7 consecutive distinct letters.
    No parameters. Prints the result and returns None.

    Method / Math Rationale
    -----------------------
    Models the problem using a state machine with 8 states: states 0 to 6
    represent the length of the current run of distinct letters at the end
    (state 0 is initial), and state 7 is an absorbing state for strings that
    have contained a forbidden substring. A transition matrix M is constructed
    where M[i][j] is the number of ways to transition from state i to j by
    adding one letter. The matrix is raised to the power n using binary
    exponentiation under modulo 10^9 to compute the number of ways to reach
    each state after n letters. The total strings is (M^n)[7][7], the invalid
    ones is (M^n)[0][7], and T(n) is their difference modulo 10^9.

    Complexity
    ----------
    O(8^3 log n) time and O(8^2) space for matrix exponentiation.

    References
    ----------
    https://projecteuler.net/problem=458
    """
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