# Problem: https://projecteuler.net/problem=172
import math
from itertools import product
from tqdm import tqdm

factorials = [math.factorial(i) for i in range(19)]
eighteen_factorial = factorials[18]
seventeen_factorial = factorials[17]

number_of_digit_types = 10
maximum_frequency_per_digit = 3
desired_number_length = 18
total_valid_numbers = 0

frequency_options = range(maximum_frequency_per_digit + 1)
total_possible_frequency_combinations = (maximum_frequency_per_digit + 1) ** number_of_digit_types

for frequency_assignment in tqdm(product(frequency_options, repeat=number_of_digit_types), total=total_possible_frequency_combinations):
    total_frequency_sum = sum(frequency_assignment)
    if total_frequency_sum == desired_number_length:
        product_of_frequency_factorials = 1
        for single_frequency in frequency_assignment:
            product_of_frequency_factorials *= factorials[single_frequency]
        numbers_for_this_assignment = eighteen_factorial // product_of_frequency_factorials
        
        if frequency_assignment[0] >= 1:
            product_for_invalid = factorials[frequency_assignment[0] - 1]
            for single_frequency in frequency_assignment[1:]:
                product_for_invalid *= factorials[single_frequency]
            invalid_numbers_for_this = seventeen_factorial // product_for_invalid
            valid_numbers_for_this = numbers_for_this_assignment - invalid_numbers_for_this
        else:
            valid_numbers_for_this = numbers_for_this_assignment
        
        total_valid_numbers += valid_numbers_for_this

print(total_valid_numbers)