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
    N = 5 * 10 ** 15
    print(euler484(N))

if __name__ == "__main__":
    main()