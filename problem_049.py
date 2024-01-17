# Problem: https://projecteuler.net/problem=49

from itertools import permutations
from sympy import isprime

def find_prime_permutations():
    for i in range(1000, 10000):
        if isprime(i):
            perms = set(int("".join(p)) for p in permutations(str(i)))
            primes = sorted(p for p in perms if isprime(p) and p > 999)
            for j in range(len(primes)):
                for k in range(j+1, len(primes)):
                    diff = primes[k] - primes[j]
                    third_term = primes[k] + diff
                    if third_term in primes:
                        # Check if it's not the example given in the problem
                        if primes[j] != 1487:
                            return (primes[j], primes[k], third_term)

if __name__ == "__main__":
    prime_sequence = find_prime_permutations()
    answer = "".join(str(p) for p in prime_sequence)
    print(answer)
