# Problem: https://projecteuler.net/problem=484
import numba as nb
import numpy as np
from math import sqrt
from sympy.ntheory import primerange

def euler484(L):
    pLst = list(primerange(2, int(sqrt(L) + 1.5)))
    qLst = np.array(pLst, dtype=np.int64) ** 2
    return L - 1 + dfs(0, L, np.array(pLst, dtype=np.int64), qLst)

@nb.njit
def dfs(i0, L0, pLst, qLst):
    res = 0
    for i in range(i0, len(pLst)):
        q = qLst[i]
        L = L0 // q
        if L == 0:
            break
        p, e, g = pLst[i], 1, 1
        while L:
            gp = g
            e += 1
            if e != 1:
                if e == p:
                    g *= q
                    e = 0
                else:
                    g *= p
                c = g - gp
                res += c * L
                if L > q:
                    res += c * dfs(i + 1, L, pLst, qLst)
            L //= p
    return res

def main():
    """
    Purpose
    Compute the sum of gcd(k, k') for 1 < k <= 5*10^15, where k' is the arithmetic derivative of k.
    Parameters: None
    Returns: None (prints the result)

    Method / Math Rationale
    The arithmetic derivative k' follows the product rule. The gcd(k, k') is multiplicative.
    The sum is computed as N - 1 + contributions from powerful numbers using a recursive DFS over primes.
    For each prime power p^e (e >= 2), incremental differences f(p^e) = gcd(p^e, (p^e)') - 
    gcd(p^{e-1}, (p^{e-1})') are calculated, handling cases where p divides e by multiplying by p^2 
    and resetting the exponent counter. The recursion builds composite powerful numbers and accumulates
    the sum of f(n) * floor(N / n) for powerful n.

    Complexity
    Time: O(sqrt(N)), dominated by looping over ~sqrt(N)/log(sqrt(N)) primes and log_p(N) iterations per prime.
    Space: O(sqrt(N)/log(sqrt(N))) for storing primes.

    References
    https://projecteuler.net/problem=484
    """
    N = 5 * 10 ** 15
    print(euler484(N))

if __name__ == "__main__":
    main()