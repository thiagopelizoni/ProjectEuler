# Problem: https://projecteuler.net/problem=132
import itertools
from sympy import isprime, mod_inverse

def main():
    condition = lambda number: isprime(number) and repunit_mod(10**9, number) == 0
    result = sum(itertools.islice(filter(condition, itertools.count(2)), 40))
    return str(result)

def repunit_mod(k, m):
    return (pow(10, k, m * 9) - 1) // 9

if __name__ == "__main__":
    print(main())