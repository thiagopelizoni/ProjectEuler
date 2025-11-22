# Problem: https://projecteuler.net/problem=291
import math

from sympy.ntheory import isprime
from tqdm import tqdm

def main():
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