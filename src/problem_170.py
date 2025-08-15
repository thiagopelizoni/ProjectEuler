# Problem: https://projecteuler.net/problem=170
import itertools
import math
from tqdm import tqdm

all_possible_digits = [str(i) for i in range(9, -1, -1)]

for digit_permutation in tqdm(itertools.permutations(all_possible_digits)):
    concatenated_product = ''.join(digit_permutation)
    
    for split_position in range(1, 10):
        first_part = concatenated_product[:split_position]
        second_part = concatenated_product[split_position:]
        
        if ((len(first_part) > 1 and first_part[0] == '0') or 
                (len(second_part) > 1 and second_part[0] == '0')):
            continue
        
        first_number = int(first_part)
        second_number = int(second_part)
        
        if str(first_number) != first_part or str(second_number) != second_part:
            continue
        
        greatest_common_divisor = math.gcd(first_number, second_number)
        
        if greatest_common_divisor < 2:
            continue
        
        all_possible_divisors = set()
        
        for candidate_divisor in range(2, int(greatest_common_divisor ** 0.5) + 1):
            if greatest_common_divisor % candidate_divisor == 0:
                all_possible_divisors.add(candidate_divisor)
                all_possible_divisors.add(greatest_common_divisor // candidate_divisor)
        
        if greatest_common_divisor >= 2:
            all_possible_divisors.add(greatest_common_divisor)
        
        for common_factor in all_possible_divisors:
            first_multiplicand = first_number // common_factor
            second_multiplicand = second_number // common_factor
            
            str_common_factor = str(common_factor)
            str_first_multiplicand = str(first_multiplicand)
            str_second_multiplicand = str(second_multiplicand)
            
            if ((len(str_first_multiplicand) > 1 and str_first_multiplicand[0] == '0') or 
                    (len(str_second_multiplicand) > 1 and str_second_multiplicand[0] == '0')):
                continue
            
            combined_digits = str_common_factor + str_first_multiplicand + str_second_multiplicand
            
            if len(combined_digits) != 10:
                continue
            
            expected_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            if sorted(combined_digits) == expected_digits:
                print(concatenated_product)
                exit()