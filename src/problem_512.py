# Problem: https://projecteuler.net/problem=512
import numba
import numpy as np

def main():
    n = 500000000
    max_odd = 499999999
    M = 250000000

    @numba.njit
    def compute_sum(M):
        phi = np.zeros(M, dtype=numba.uint64)
        for i in range(M):
            phi[i] = 2 * (i + 1) - 1
        for i in range(1, M):
            if phi[i] == 2 * i + 1:
                p = phi[i]
                j = i
                while j < M:
                    phi[j] = (phi[j] // p) * (p - 1)
                    j += p
        s = numba.uint64(0)
        for i in range(M):
            s += phi[i]
        return s

    result = compute_sum(M)
    print(result)

if __name__ == "__main__":
    main()