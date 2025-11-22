# Problem: https://projecteuler.net/problem=498
def comb_mod(a, b, mod):
    if b < 0 or b > a:
        return 0
    if b > a - b:
        b = a - b
    res = 1
    for i in range(b):
        res = (res * (a - i)) % mod
        res = (res * pow(i + 1, mod - 2, mod)) % mod
    return res

def main():
    n = 10**13
    m = 10**12
    d = 10**4
    mod = 999999937
    first = comb_mod(n, d, mod)
    q = n - d - 1
    r = m - d - 1
    q1 = q // mod
    q0 = q % mod
    r1 = r // mod
    r0 = r % mod
    second = (comb_mod(q1, r1, mod) * comb_mod(q0, r0, mod)) % mod
    result = (first * second) % mod
    print(result)

if __name__ == "__main__":
    main()