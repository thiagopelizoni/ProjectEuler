# Problem: https://projecteuler.net/problem=323
from fractions import Fraction
from math import comb
from decimal import Decimal

def main():
    """
    Purpose:
    Computes the expected number of operations to set all 32 bits to 1 using random OR operations
    and prints it rounded to 10 decimal places.

    Method / Math Rationale:
    The number of operations is the maximum of 32 independent geometric random variables with
    success probability 1/2. The expectation is calculated as the sum from j=1 to 32 of
    comb(32, j) * (-1)**(j+1) * (2**j / (2**j - 1)), derived from the binomial expansion of the
    survival function in the expression for the expected value of the maximum.

    Complexity:
    O(32) time and space, effectively constant.

    References:
    https://projecteuler.net/problem=323
    """
    expectation = Fraction(0)
    for j in range(1, 33):
        sign = 1 if j % 2 == 1 else -1
        term = comb(32, j) * sign * Fraction(2**j, 2**j - 1)
        expectation += term
    dec = Decimal(expectation.numerator) / Decimal(expectation.denominator)
    print(f"{dec:.10f}")

if __name__ == "__main__":
    main()