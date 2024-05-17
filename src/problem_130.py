# Problem: https://projecteuler.net/problem=130
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

def find_composite_nonprime_repunit_divisors(limit):
    result = []
    n = 2
    while len(result) < limit:
        if not sympy.isprime(n) and sympy.gcd(n, 10) == 1:
            if (n - 1) % A(n) == 0:
                result.append(n)
        n += 1
    return result

if __name__ == '__main__':  
    limit = 25
    result = find_composite_nonprime_repunit_divisors(limit)
    answer = sum(result)
    print(answer)
