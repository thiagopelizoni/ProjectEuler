# Problem: https://projecteuler.net/problem=129
import sympy

def A(n):
    if sympy.gcd(n, 10) != 1:
        return 0
    k = 1
    r = 1
    while r != 0:
        r = (r * 10 + 1) % n
        k += 1
    return k

def find_min_n(limit):
    n = limit
    while True:
        if A(n) > limit:
            return n
        n += 1

if __name__ == '__main__':
    limit = 1000000
    result = find_min_n(limit)
    print(result)
