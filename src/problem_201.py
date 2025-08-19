# Problem: https://projecteuler.net/problem=201
import numpy as np
from tqdm import tqdm

squares_list = []
for number in range(1, 101):
    squares_list.append(number * number)

largest_fifty_squares_sum = sum(squares_list[-50:])
array_length = largest_fifty_squares_sum + 1

ways_array = np.zeros((51, array_length), dtype=np.uint8)
ways_array[0, 0] = 1

for current_square in tqdm(squares_list):
    new_ways_array = ways_array.copy()
    for current_item_count in range(50):
        shift_amount = current_square
        source_slice = ways_array[current_item_count, :array_length - shift_amount]
        target_slice = new_ways_array[current_item_count + 1, shift_amount:]
        target_slice += source_slice
        np.minimum(target_slice, 2, out=target_slice)
    ways_array = new_ways_array

sum_positions = np.arange(array_length)
unique_locations = (ways_array[50] == 1)
unique_subset_sums = sum_positions[unique_locations]
total_of_unique_sums = np.sum(unique_subset_sums)

print(total_of_unique_sums)