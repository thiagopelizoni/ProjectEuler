# Problem: https://projecteuler.net/problem=71
from fractions import Fraction

# maximum denominator
max_denominator = 1000000

# Target fraction
target_fraction = Fraction(3, 7)

# Default fraction that is smaller than the target
left_neighbor = Fraction(0, 1)

# Iterate over the denominators
for d in range(2, max_denominator + 1):
    # Calculate the numerator that makes the fraction just smaller than the target
    n = (target_fraction.numerator * d) // target_fraction.denominator

    # Construct the fraction and ensure it is a reduced proper fraction
    fraction = Fraction(n, d)
    if fraction < target_fraction and fraction > left_neighbor:
        left_neighbor = fraction

# Answer: the numerator of the fraction immediately to the left of 3/7
print(left_neighbor.numerator)
