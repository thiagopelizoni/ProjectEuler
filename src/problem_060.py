# Problem: https://projecteuler.net/problem=60
# Failed attempt to silve this problem
from sympy import primerange
from itertools import permutations

def is_prime_concat(set_primes, a, b):
    return (int(str(a) + str(b)) in set_primes) and (int(str(b) + str(a)) in set_primes)

def find_prime_set():
    primes = list(primerange(3, 10000))
    set_primes = set(primes)

    for a in primes:
        for b in [x for x in primes if x > a and is_prime_concat(set_primes, a, x)]:
            for c in [x for x in primes if x > b and is_prime_concat(set_primes, a, x) and is_prime_concat(set_primes, b, x)]:
                for d in [x for x in primes if x > c and is_prime_concat(set_primes, a, x) and is_prime_concat(set_primes, b, x) and is_prime_concat(set_primes, c, x)]:
                    for e in [x for x in primes if x > d and is_prime_concat(set_primes, a, x) and is_prime_concat(set_primes, b, x) and is_prime_concat(set_primes, c, x) and is_prime_concat(set_primes, d, x)]:
                        return a + b + c + d + e

answer = find_prime_set()
print(answer)
