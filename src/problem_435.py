# Problem: https://projecteuler.net/problem=435
from tqdm import tqdm

def mat_mult(A, B, mod):
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def mat_pow(base, exp, mod):
    result = [[1, 0], [0, 1]]
    while exp > 0:
        if exp % 2 == 1:
            result = mat_mult(result, base, mod)
        base = mat_mult(base, base, mod)
        exp //= 2
    return result

def fib(n, mod):
    if n == 0:
        return 0
    if n == 1:
        return 1
    T = [[1, 1], [1, 0]]
    powered = mat_pow(T, n - 1, mod)
    return powered[0][0]

def main():
    """
    Purpose
    -------
    Computes the sum of F_n(x) for x from 0 to 100, where F_n(x) is the polynomial
    sum_{i=0}^n f_i x^i with Fibonacci numbers f_i (f_0=0, f_1=1, ...), for
    n=10^15, modulo 1307674368000 (15!).

    Method / Math Rationale
    -----------------------
    Uses the closed-form expression for F_n(x) = (f_n x^{n+2} + f_{n+1} x^{n+1} - x)
    / (x^2 + x - 1).
    To compute modulo m, calculates the numerator modulo m * |denominator|, then
    performs integer division by |denominator|, and adjusts sign if necessary.
    Fibonacci numbers are computed using matrix exponentiation modulo the large
    modulus. Powers are computed using built-in pow with modulus.

    Complexity
    ----------
    Time: O(100 * log(n)) due to matrix exponentiations and modular powers for each x.
    Space: O(1)

    References
    ----------
    https://projecteuler.net/problem=435
    https://bin.re/blog/project-euler-problem-435-polynomials-of-fibonacci-numbers/
    """
    n = 10**15
    m = 1307674368000
    total = 0

    for x in tqdm(range(101)):
        b = x * x + x - 1
        abs_b = abs(b)
        modulus = m * abs_b
        f_n = fib(n, modulus)
        f_nn = fib(n + 1, modulus)
        xp1 = pow(x, n + 1, modulus)
        xp2 = (xp1 * x) % modulus
        num = (f_n * xp2 + f_nn * xp1 - x) % modulus
        q = num // abs_b
        if b < 0:
            fn_x = (-q) % m
        else:
            fn_x = q % m
        total = (total + fn_x) % m

    print(total)

if __name__ == "__main__":
    main()