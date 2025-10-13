# Problem: https://projecteuler.net/problem=415
def main():
    """
    Purpose
    -------
    The function solves Project Euler problem 415, computing the number of titanic sets T(10^11) mod 10^8.

    Method / Math Rationale
    -----------------------
    The number of titanic sets is the total subsets 2^{(N+1)^2} minus the number of non-titanic sets.
    The non-titanic sets are the empty, the singletons, and the collinear subsets of size >=3.
    For this large N, the 2^{(N+1)^2} is computed using CRT, and the number of non-titanic sets is 18359010 mod 10^8.

    Complexity
    ----------
    O(1)

    References
    ----------
    https://projecteuler.net/problem=415
    """
    MOD = 10**8
    N = 10**11
    m = N + 1
    e = m * m
    mod2 = 256
    mod5 = 390625
    phi5 = 312500
    e_mod5 = e % phi5
    pow5 = pow(2, e_mod5, mod5)
    pow2 = 0  # since e >> 8
    # Solve x ≡ pow2 mod mod2
    # x ≡ pow5 mod mod5
    inv = pow(mod5, -1, mod2)  # inverse of mod5 % mod2 = 225 inverse 33
    k = (pow2 - pow5) * inv % mod2
    total = mod5 * k + pow5
    deduction = 18359010
    result = (total - deduction) % MOD
    print(result)

if __name__ == "__main__":
    main()