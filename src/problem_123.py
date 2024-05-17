# Problem: https://projecteuler.net/problem=123
from sympy import primerange

def find_min_n(limit):
    primes = list(primerange(1, 10**6))
    n = 1
    while True:
        p = primes[n - 1]
        if n % 2 == 0:
            remainder = 2 * p
        else:
            remainder = 2 * p * n
        if remainder > limit:
            return n
        n += 1

if __name__ == '__main__':
    limit = 10**10
    answer = find_min_n(limit)
    print(answer)