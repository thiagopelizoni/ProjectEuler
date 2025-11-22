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