# Problem: https://projecteuler.net/problem=242
from tqdm import tqdm

T = 249999999999
binary_string = bin(T)[2:]
digits_list = [int(digit) for digit in binary_string]
number_of_bits = len(digits_list)

dp_table = [[0] * 2 for _ in range(number_of_bits + 1)]
dp_table[number_of_bits][0] = 1
dp_table[number_of_bits][1] = 1

for position in tqdm(range(number_of_bits - 1, -1, -1)):
    for is_tight in [0, 1]:
        upper_limit = digits_list[position] if is_tight else 1
        accumulated_sum = 0
        for current_digit in range(upper_limit + 1):
            new_is_tight = 1 if is_tight and current_digit == upper_limit else 0
            contribution = 2 if current_digit == 1 else 1
            accumulated_sum += contribution * dp_table[position + 1][new_is_tight]
        dp_table[position][is_tight] = accumulated_sum

print(dp_table[0][1])