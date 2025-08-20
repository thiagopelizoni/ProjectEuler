# Problem: https://projecteuler.net/problem=211
import numpy as np
from tqdm import tqdm
import math
from multiprocessing import Pool, cpu_count

upper_limit_n = 64000000

def compute_partial_contributions(process_index, total_processes):
    partial_sigma_array = np.zeros(upper_limit_n, dtype=np.uint64)
    for divisor in range(process_index + 1, upper_limit_n, total_processes):
        partial_sigma_array[divisor::divisor] += divisor ** 2
    return partial_sigma_array

number_of_processes = cpu_count()
with Pool(number_of_processes) as pool_object:
    partial_arrays_list = pool_object.starmap(compute_partial_contributions, [(i, number_of_processes) for i in range(number_of_processes)])

sum_of_squares_of_divisors = np.sum(partial_arrays_list, axis=0)

total_sum_of_qualifying_numbers = 0
for current_number in tqdm(range(1, upper_limit_n)):
    current_sigma_value = sum_of_squares_of_divisors[current_number]
    integer_square_root = math.isqrt(current_sigma_value)
    if integer_square_root * integer_square_root == current_sigma_value:
        total_sum_of_qualifying_numbers += current_number

print(total_sum_of_qualifying_numbers)