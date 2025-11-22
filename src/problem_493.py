# Problem: https://projecteuler.net/problem=493
from decimal import Decimal, getcontext
from fractions import Fraction

def main():
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