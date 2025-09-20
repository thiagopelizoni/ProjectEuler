# Problem: https://projecteuler.net/problem=335
from math import pow as math_pow  # not needed, but to follow

def main():
    """
    Purpose
    -------
    Solves Problem 335 from Project Euler: Gathering the beans.
    Computes the sum of M(2^k + 1) for k from 0 to 10^18, modulo 7^9.

    Method / Math Rationale
    -----------------------
    Simulation for small values reveals that M(2^k + 1) = 2^{k+1} + 4^k - 3^k.
    The sum S = sum_{k=0}^N (2^{k+1} + 4^k - 3^k) = 2 * (2^{N+1} - 1) + (4^{N+1} - 1)/3 - (3^{N+1} - 1)/2,
    where N = 10^18. This is computed using modular exponentiation and modular inverses.

    Complexity
    ----------
    Time complexity: O(log N) due to modular exponentiations
    Space complexity: O(1)

    References
    ----------
    https://projecteuler.net/problem=335
    """
    N = 10**18
    MOD = 7**9
    pow2_N1 = pow(2, N + 1, MOD)
    pow3_N1 = pow(3, N + 1, MOD)
    pow4_N1 = pow(4, N + 1, MOD)
    inv2 = pow(2, -1, MOD)
    inv3 = pow(3, -1, MOD)
    term1 = 2 * (pow2_N1 - 1) % MOD
    term2 = (pow4_N1 - 1) * inv3 % MOD
    term3 = (pow3_N1 - 1) * inv2 % MOD
    result = (term1 + term2 - term3 + 2 * MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()