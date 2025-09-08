# Problem: https://projecteuler.net/problem=291
import math

from sympy.ntheory import isprime
from tqdm import tqdm

def main():
    """
    Purpose
    Count the number of Panaitopol primes less than 5*10^15, where a Panaitopol prime is a prime of the form 2n^2 + 2n + 1
    for positive integer n.

    Method / Math Rationale
    Simplify the expression (x^4 - y^4)/(x^3 + y^3) to show that such primes are exactly the primes of the form
    n^2 + (n+1)^2 = 2n^2 + 2n + 1.
    Compute the maximum n such that 2n^2 + 2n + 1 < 5*10^15 using the quadratic formula.
    Then iterate over n from 1 to max_n, check if the number is prime using sympy's isprime.

    Complexity
    Time: O(max_n * t), where t is the time for isprime, which is polylog for each call. With max_n ~ 5*10^7,
    practical runtime is acceptable.
    Space: O(1)

    References
    https://projecteuler.net/problem=291
    """
    limit = 5 * 10**15
    disc = 1 + 2 * (limit - 1)
    sqrt_disc = math.sqrt(disc)
    max_n = int((-1 + sqrt_disc) / 2)
    while 2 * max_n * max_n + 2 * max_n + 1 >= limit:
        max_n -= 1
    count = 0
    for n in tqdm(range(1, max_n + 1)):
        p = 2 * n * n + 2 * n + 1
        if isprime(p):
            count += 1
    print(count)

if __name__ == "__main__":
    main()