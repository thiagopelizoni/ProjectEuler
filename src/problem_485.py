# Problem: https://projecteuler.net/problem=485
import numpy as np
from sympy.ntheory import primerange
from tqdm import tqdm

def count_divisors(limit, prime_limit):
    num_divisors = np.ones(limit + 1, dtype=np.uint16)
    num_divisors[0] = 0
    primes = list(primerange(2, prime_limit + 1))
    for p in primes:
        if p > limit:
            break
        num_divisors[p::p] *= 2
        power = p * p
        exponent = 2
        while power <= limit:
            num_divisors[power::power] = (
                num_divisors[power::power] // exponent
            ) * (exponent + 1)
            power *= p
            exponent += 1
    return num_divisors

def compute_s(u, k, num_divisors):
    most_recent = []
    for i in range(1, k + 1):
        current = num_divisors[i]
        if current >= len(most_recent):
            most_recent += [0] * (current - len(most_recent) + 1)
        most_recent[current] = i
    result = len(most_recent) - 1
    for i in tqdm(range(k + 1, u + 1)):
        too_far = i - k
        while most_recent and most_recent[-1] <= too_far:
            most_recent.pop()
        current = num_divisors[i]
        if current >= len(most_recent):
            most_recent += [0] * (current - len(most_recent) + 1)
        most_recent[current] = i
        result += len(most_recent) - 1
    return result

def main():
    u = 100000000
    k = 100000
    prime_limit = int(u**0.5) + 1
    num_divisors = count_divisors(u, prime_limit)
    s = compute_s(u, k, num_divisors)
    print(s)

if __name__ == "__main__":
    main()