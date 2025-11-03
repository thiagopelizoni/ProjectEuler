# Problem: https://projecteuler.net/problem=473
from math import gcd

def get_F(i, F):
    if i >= 0:
        return F[i]
    n = -i
    return (-1)**(n+1) * F[n]

def get_L(i, L):
    if i >= 0:
        return L[i]
    n = -i
    return (-1)**n * L[n]

def search_skewed(limit, max_exp, F, L, exponent=0, sum_L=0, sum_F=0):
    if sum_L > 2 * limit:
        return 0
    result = 0
    if sum_F == 0:
        n = sum_L // 2
        if 1 <= n <= limit:
            result += n
    if exponent == 0:
        exponent = 1
    else:
        exponent += 2
    while exponent <= max_exp:
        pos = exponent
        neg = -(exponent + 1)
        new_L = sum_L + get_L(pos, L) + get_L(neg, L)
        new_F = sum_F + get_F(pos, F) + get_F(neg, F)
        result += search_skewed(limit, max_exp, F, L, exponent + 1, new_L, new_F)
        exponent += 1
    return result

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 473: Find the sum of all positive integers not exceeding 10^10 whose
    phigital representation is palindromic.

    Method / Math Rationale
    ------------------------
    Uses a recursive search to generate candidate sets of exponents for skewed pairs (k, -k-1) with minimum
    difference 3 between k's, computes the sum using Lucas numbers for the rational part and Fibonacci for
    the irrational part, adding the n if the irrational part cancels (sum_F = 0).

    Complexity
    ----------
    O(1.465^48) time, approximately 10^8 operations.

    References
    ----------
    https://projecteuler.net/problem=473
    """
    limit = 10**10
    max_exp = 48
    F = [0] * (max_exp + 3)
    F[0] = 0
    F[1] = 1
    for i in range(2, len(F)):
        F[i] = F[i-1] + F[i-2]

    L = [0] * (max_exp + 3)
    L[0] = 2
    L[1] = 1
    for i in range(2, len(L)):
        L[i] = L[i-1] + L[i-2]

    total = search_skewed(limit, max_exp, F, L) + 1
    print(total)

if __name__ == "__main__":
    main()