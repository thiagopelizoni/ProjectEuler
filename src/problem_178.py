# Problem: https://projecteuler.net/problem=178
from tqdm import tqdm

NUM_DIGITS = 10
FULL_MASK = (1 << NUM_DIGITS) - 1
MAX_LENGTH = 40

dp = [[[0 for _ in range(1 << NUM_DIGITS)] for _ in range(NUM_DIGITS)] for _ in range(MAX_LENGTH + 1)]

for first_digit in range(1, NUM_DIGITS):
    mask_for_first = 1 << first_digit
    dp[1][first_digit][mask_for_first] = 1

for current_length in tqdm(range(1, MAX_LENGTH)):
    for last_digit in range(NUM_DIGITS):
        for used_mask in range(1 << NUM_DIGITS):
            ways_so_far = dp[current_length][last_digit][used_mask]
            if ways_so_far == 0:
                continue
            for delta in [-1, 1]:
                next_digit = last_digit + delta
                if 0 <= next_digit < NUM_DIGITS:
                    new_used_mask = used_mask | (1 << next_digit)
                    dp[current_length + 1][next_digit][new_used_mask] += ways_so_far

total_pandigital_step_numbers = 0
for length in range(NUM_DIGITS, MAX_LENGTH + 1):
    for last_digit in range(NUM_DIGITS):
        total_pandigital_step_numbers += dp[length][last_digit][FULL_MASK]

print(total_pandigital_step_numbers)