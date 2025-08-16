# Problem: https://projecteuler.net/problem=178
from tqdm import tqdm


number_of_digits = 10
full_digit_mask = (1 << number_of_digits) - 1
max_length = 40


count_paths = [
    [
        [0 for _ in range(1 << number_of_digits)]
        for _ in range(number_of_digits)
    ]
    for _ in range(max_length + 1)
]


for first_digit in range(1, number_of_digits):
    initial_mask = 1 << first_digit
    count_paths[1][first_digit][initial_mask] = 1


for current_length in tqdm(range(1, max_length)):
    for ending_digit in range(number_of_digits):
        for used_digits_mask in range(1 << number_of_digits):
            path_count = count_paths[current_length][ending_digit][
                used_digits_mask
            ]
            if path_count == 0:
                continue
            for step_direction in (-1, 1):
                next_digit = ending_digit + step_direction
                if 0 <= next_digit < number_of_digits:
                    new_used_digits_mask = used_digits_mask | (1 << next_digit)
                    count_paths[current_length + 1][next_digit][
                        new_used_digits_mask
                    ] += path_count


total_pandigital_step_numbers = 0

for length_value in range(number_of_digits, max_length + 1):
    for ending_digit in range(number_of_digits):
        total_pandigital_step_numbers += count_paths[length_value][
            ending_digit
        ][full_digit_mask]


print(total_pandigital_step_numbers)
