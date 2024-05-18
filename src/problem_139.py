# Problem: https://projecteuler.net/problem=139
from math import gcd, isqrt

def main():
    perimeter = 100000000
    total = 0

    for n in range(1, isqrt(perimeter // 2)):
        for m in range(n + 1, isqrt(perimeter - n * n) + 1, 2):
            if gcd(n, m) != 1:
                continue

            a, b, c = m * m - n * n, 2 * m * n, m * m + n * n

            if a > b:
                a, b = b, a

            if c % (b - a) == 0:
                total += perimeter // (a + b + c)

    print(total)

if __name__ == "__main__":
    main()
