# Problem: https://projecteuler.net/problem=171
import numpy as np
from tqdm import tqdm

modulo = 1000000000
total_digits = 20
low_digits_count = 9
high_digits_count = total_digits - low_digits_count
max_sum_squares_high = high_digits_count * 81
max_sum_squares_low = low_digits_count * 81

high_digit_ways = np.zeros((high_digits_count + 1, max_sum_squares_high + 1), dtype=np.int64)
high_digit_ways[0][0] = 1

for current_layer in tqdm(range(high_digits_count)):
    for current_sum_squares in range(max_sum_squares_high + 1):
        ways_so_far = high_digit_ways[current_layer][current_sum_squares]
        if ways_so_far > 0:
            for digit_choice in range(10):
                new_sum_squares = current_sum_squares + digit_choice ** 2
                if new_sum_squares <= max_sum_squares_high:
                    high_digit_ways[current_layer + 1][new_sum_squares] += ways_so_far

low_digit_ways = np.zeros((low_digits_count + 1, max_sum_squares_low + 1), dtype=np.int64)
low_digit_sums = np.zeros((low_digits_count + 1, max_sum_squares_low + 1), dtype=np.int64)

low_digit_ways[0][0] = 1
low_digit_sums[0][0] = 0

for current_layer in tqdm(range(1, low_digits_count + 1)):
    place_multiplier = 10 ** (current_layer - 1)
    for current_sum_squares in range(max_sum_squares_low + 1):
        ways_so_far = low_digit_ways[current_layer - 1][current_sum_squares]
        if ways_so_far > 0:
            sums_so_far = low_digit_sums[current_layer - 1][current_sum_squares]
            for digit_choice in range(10):
                new_sum_squares = current_sum_squares + digit_choice ** 2
                if new_sum_squares <= max_sum_squares_low:
                    low_digit_ways[current_layer][new_sum_squares] += ways_so_far
                    low_digit_sums[current_layer][new_sum_squares] += sums_so_far + ways_so_far * digit_choice * place_multiplier

perfect_squares_list = [i ** 2 for i in range(41)]

total_accumulated = 0

for sum_squares_high in range(max_sum_squares_high + 1):
    ways_high = high_digit_ways[high_digits_count][sum_squares_high]
    if ways_high == 0:
        continue

    for perfect_square in perfect_squares_list:
        if perfect_square >= sum_squares_high:
            target_sum_low = perfect_square - sum_squares_high
            if target_sum_low <= max_sum_squares_low:
                sum_values_low = low_digit_sums[low_digits_count][target_sum_low]
                contribution = (int(ways_high) * int(sum_values_low)) % modulo
                total_accumulated = (total_accumulated + contribution) % modulo

print(total_accumulated)