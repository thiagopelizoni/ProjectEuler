# Problem: https://projecteuler.net/problem=493
from decimal import Decimal, getcontext
from fractions import Fraction

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 493: Compute the expected number of distinct colors in 20 randomly
    picked balls from an urn with 70 balls (10 each of 7 colors).

    Method / Math Rationale
    -----------------------
    Uses linearity of expectation. For each color, the probability it appears is 1 -
    binom(60,20)/binom(70,20). The expected value is 7 times this probability. The ratio is computed
    exactly using Fraction by multiplying terms (60-i)/(70-i) for i=0 to 19.

    Complexity
    ----------
    O(1) time and space (fixed loops).

    References
    ----------
    https://projecteuler.net/problem=493
    """
    colors = 7
    balls_per_color = 10
    picks = 20
    total_balls = colors * balls_per_color
    prob_none = Fraction(1)
    for i in range(picks):
        prob_none *= Fraction(total_balls - balls_per_color - i, total_balls - i)
    prob_at_least_one = 1 - prob_none
    expected = colors * prob_at_least_one
    getcontext().prec = 20
    result = Decimal(expected.numerator) / Decimal(expected.denominator)
    print(f"{result:.9f}")

if __name__ == "__main__":
    main()