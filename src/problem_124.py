# Problem: https://projecteuler.net/problem=124
import sympy
import numpy as np

def prime_factors(n):
    return sympy.primefactors(n)

def rad(n):
    factors = prime_factors(n)
    product = 1
    for factor in factors:
        product *= factor
    return product

def sorted_radicals(limit, k):
    radicals = [(i, rad(i)) for i in range(1, limit + 1)]
    radicals.sort(key=lambda x: (x[1], x[0]))
    return radicals[k - 1][0]

if __name__ == '__main__':
    limit = 100000
    k = 10000
    result = sorted_radicals(limit, k)
    print(result)
