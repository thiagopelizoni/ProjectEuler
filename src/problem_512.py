# Problem: https://projecteuler.net/problem=512
import numba
import numpy as np

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 512: compute g(500000000), where g(n) is the sum from i=1 to n of f(i),
    and f(i) = (sum from j=1 to i of phi(i^j)) mod (i+1), with phi being Euler's totient function.
    No parameters.
    Prints the result.

    Method / Math Rationale
    ----------------------
    It is derived that f(n) = 0 if n is even, and phi(n) if n is odd, since phi(n) < n+1 for all n.
    Thus, g(n) = sum of phi(k) over all odd k <= n.
    A specialized sieve is used to compute phi for all odd numbers up to n, then sum them.

    Complexity
    ----------
    O(n log log n) time, O(n/2) space.

    References
    ----------
    https://projecteuler.net/problem=512
    """
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