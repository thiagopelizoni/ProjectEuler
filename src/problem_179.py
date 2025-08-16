# Problem: https://projecteuler.net/problem=179
import numpy as np
from tqdm import tqdm

upper_limit = 10**7
divisor_counts_array = np.zeros(upper_limit + 1, dtype=int)

for current_factor in tqdm(range(1, upper_limit + 1)):
    for multiple in range(current_factor, upper_limit + 1, current_factor):
        divisor_counts_array[multiple] += 1

matching_pairs_count = 0
for number in range(2, upper_limit):
    if divisor_counts_array[number] == divisor_counts_array[number + 1]:
        matching_pairs_count += 1

print(matching_pairs_count)