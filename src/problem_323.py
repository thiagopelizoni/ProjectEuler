# Problem: https://projecteuler.net/problem=323
from fractions import Fraction
from math import comb
from decimal import Decimal

def main():
    expectation = Fraction(0)
    for j in range(1, 33):
        sign = 1 if j % 2 == 1 else -1
        term = comb(32, j) * sign * Fraction(2**j, 2**j - 1)
        expectation += term
    dec = Decimal(expectation.numerator) / Decimal(expectation.denominator)
    print(f"{dec:.10f}")

if __name__ == "__main__":
    main()