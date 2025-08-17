# Problem: https://projecteuler.net/problem=180
import math
from fractions import Fraction
from tqdm import tqdm

max_order = 35
all_rationals_set = set()
for denominator in range(2, max_order + 1):
    for numerator in range(1, denominator):
        all_rationals_set.add(Fraction(numerator, denominator))
rationals_sorted_list = sorted(list(all_rationals_set))

def is_perfect_square(number):
    if number < 0:
        return False

    root_value = int(math.sqrt(number))
    return root_value * root_value == number

def compute_rational_sqrt(rational_value):
    if rational_value == 0:
        return Fraction(0)

    numerator_value = rational_value.numerator
    denominator_value = rational_value.denominator
    if not is_perfect_square(numerator_value) or not is_perfect_square(denominator_value):
        return None

    sqrt_numerator = int(math.sqrt(numerator_value))
    sqrt_denominator = int(math.sqrt(denominator_value))
    return Fraction(sqrt_numerator, sqrt_denominator)

distinct_sums_set = set()

for first_rational in tqdm(rationals_sorted_list):
    for second_rational in rationals_sorted_list:
        # Case for n = -2
        sum_of_squares = first_rational ** 2 + second_rational ** 2
        sqrt_sum_squares = compute_rational_sqrt(sum_of_squares)
        if sqrt_sum_squares is not None and sqrt_sum_squares != 0:
            third_rational = (first_rational * second_rational) / sqrt_sum_squares
            if third_rational in all_rationals_set:
                distinct_sums_set.add(first_rational + second_rational + third_rational)

        # Case for n = -1
        sum_first_second = first_rational + second_rational
        if sum_first_second != 0:
            third_rational = (first_rational * second_rational) / sum_first_second
            if third_rational in all_rationals_set:
                distinct_sums_set.add(first_rational + second_rational + third_rational)

        # Case for n = 1
        third_rational = first_rational + second_rational
        if third_rational in all_rationals_set:
            distinct_sums_set.add(first_rational + second_rational + third_rational)

        # Case for n = 2
        sqrt_sum_squares = compute_rational_sqrt(first_rational ** 2 + second_rational ** 2)
        if sqrt_sum_squares is not None:
            third_rational = sqrt_sum_squares
            if third_rational in all_rationals_set:
                distinct_sums_set.add(first_rational + second_rational + third_rational)

total_sum_value = sum(distinct_sums_set)
numerator_part = total_sum_value.numerator
denominator_part = total_sum_value.denominator
print(numerator_part + denominator_part)