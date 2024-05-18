# Problem: https://projecteuler.net/problem=128
import itertools
from sympy import isprime

def main():
    target = 2000
    prime_count = 2
    for ring_number in itertools.count(2):
        if all(map(isprime, (ring_number * 6 - 1, ring_number * 6 + 1, ring_number * 12 + 5))):
            prime_count += 1
            if prime_count == target:
                return str(ring_number * (ring_number - 1) * 3 + 2)
        if all(map(isprime, (ring_number * 6 - 1, ring_number * 6 + 5, ring_number * 12 - 7))):
            prime_count += 1
            if prime_count == target:
                return str(ring_number * (ring_number + 1) * 3 + 1)

if __name__ == "__main__":
    print(main())