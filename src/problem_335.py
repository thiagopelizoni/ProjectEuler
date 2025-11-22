# Problem: https://projecteuler.net/problem=335
from math import pow as math_pow  # not needed, but to follow

def main():
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