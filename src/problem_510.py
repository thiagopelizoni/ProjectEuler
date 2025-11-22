# Problem: https://projecteuler.net/problem=510
import math
from tqdm import tqdm

def triangle(n):
    return n * (n + 1) // 2

def main():
    n = 10**9
    result = 0
    max_a = math.isqrt(n)
    for a in tqdm(range(1, max_a + 1)):
        a2 = a * a
        for b in range(1, a + 1):
            b2 = b * b
            numerator = a2 * b2
            denominator = (a + b) * (a + b)
            if numerator % denominator != 0:
                continue
            c2 = numerator // denominator
            g = math.gcd(math.gcd(a2, b2), c2)
            if g == 1:
                M = n // a2
                sum_radii = a2 + b2 + c2
                contrib = sum_radii * triangle(M)
                result += contrib
    print(result)

if __name__ == "__main__":
    main()