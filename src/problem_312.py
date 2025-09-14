# Problem: https://projecteuler.net/problem=312
from sys import stderr

def mod_inverse(a, m):
    return pow(a, -1, m)

def crt(a1, m1, a2, m2):
    inv = mod_inverse(m2, m1)
    k = ((a1 - a2) * inv) % m1
    return a2 + m2 * k

def get_N(n, m, phi_m):
    if n == 1:
        return 1
    # for n >= 2
    two_phi = 2 * phi_m
    exp_base = pow(3, n - 2, two_phi)
    exp3 = (exp_base - 1) // 2
    three_part = pow(3, exp3, m)
    exp2 = pow(3, n - 2, phi_m)
    two_part = pow(2, exp2, m)
    return (two_part * three_part) % m

def main():
    """
    Purpose
    Solve Project Euler problem 312: Compute C(C(C(10000))) mod 13^8 where C(n) is the number of cyclic Hamiltonian paths on the Sierpinski graph S_n.

    Method / Math Rationale
    Derive recurrences for N(n), the number of Hamiltonian paths from one corner to another, with C(n) = N(n-1)^3.
    Use closed form expression for N(n) = 2^{3^{n-2}} * 3^{(3^{n-2}}-1)/2} mod m for n >= 2, with modular exponentiation handling large exponents.
    Use CRT to reconstruct arguments for nested evaluations using provided moduli.

    Complexity
    O(log (nested argument size)) due to modular exponentiations; practical for given sizes.

    References
    https://projecteuler.net/problem=312
    """
    m = 13**8
    phi_m = m * (1 - 1 // 13)
    a = 10000
    N9999 = get_N(a - 1, m, phi_m)
    c1 = pow(N9999, 3, m)
    m1 = 10**8
    a1 = 37652224
    m2 = m
    a2 = c1
    c1_rep = crt(a1, m1, a2, m2)
    n2 = c1_rep - 1
    N2 = get_N(n2, m, phi_m)
    c2 = pow(N2, 3, m)
    n3 = c2 - 1
    N3 = get_N(n3, m, phi_m)
    print(pow(N3, 3, m))

if __name__ == "__main__":
    main()