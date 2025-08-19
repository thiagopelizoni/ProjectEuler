# Problem: https://projecteuler.net/problem=196
import math
import multiprocessing
from collections import defaultdict
from tqdm import tqdm
import numpy as np

def get_row_start(row_number):
    return row_number * (row_number - 1) // 2 + 1

def sieve_for_small_primes(max_limit):
    is_prime = [True] * (max_limit + 1)
    is_prime[0] = is_prime[1] = False
    for number in range(2, int(math.sqrt(max_limit)) + 1):
        if is_prime[number]:
            for multiple in range(number * number, max_limit + 1, number):
                is_prime[multiple] = False
    small_primes = [number for number in range(2, max_limit + 1) if is_prime[number]]
    return small_primes

def segmented_is_prime(min_number, max_number, small_primes_list):
    array_size = max_number - min_number + 1
    is_prime_array = np.full(array_size, True)
    if min_number <= 1:
        start = max(min_number, 0) - min_number
        end = min(2, max_number + 1) - min_number
        is_prime_array[start:end] = False
    for prime in tqdm(small_primes_list):
        if prime * prime > max_number:
            break
        start_multiple = math.ceil(min_number / prime) * prime
        if start_multiple == prime:
            start_multiple += prime
        for multiple in range(max(start_multiple, prime * prime), max_number + 1, prime):
            is_prime_array[multiple - min_number] = False
    return is_prime_array

def find_parent(parent_array, prime_index):
    if parent_array[prime_index] != prime_index:
        parent_array[prime_index] = find_parent(parent_array, parent_array[prime_index])
    return parent_array[prime_index]

def union_sets(parent_array, prime_index_one, prime_index_two):
    parent_one = find_parent(parent_array, prime_index_one)
    parent_two = find_parent(parent_array, prime_index_two)
    if parent_one != parent_two:
        parent_array[parent_one] = parent_two

def compute_s_for_row(target_row):
    start_row_number = target_row - 2
    end_row_number = target_row + 2
    min_number_in_range = get_row_start(start_row_number)
    max_number_in_range = get_row_start(end_row_number + 1) - 1
    array_size = max_number_in_range - min_number_in_range + 1
    square_root_max = int(math.sqrt(max_number_in_range)) + 1
    small_primes_list = sieve_for_small_primes(square_root_max)
    is_prime_array = segmented_is_prime(min_number_in_range, max_number_in_range, small_primes_list)
    row_numbers_list = list(range(start_row_number, end_row_number + 1))
    row_lengths_list = [row for row in row_numbers_list]
    row_start_indices_list = [0]
    for length in row_lengths_list[:-1]:
        row_start_indices_list.append(row_start_indices_list[-1] + length)
    prime_numbers_list = []
    prime_positions_dict = {}
    row_of_each_prime_list = []
    current_row_index = 0
    current_row_start_index = 0
    for array_index in range(array_size):
        while array_index >= current_row_start_index + row_lengths_list[current_row_index]:
            current_row_start_index += row_lengths_list[current_row_index]
            current_row_index += 1
        if is_prime_array[array_index]:
            column_number = array_index - current_row_start_index + 1
            row_number = row_numbers_list[current_row_index]
            current_number = min_number_in_range + array_index
            prime_index = len(prime_numbers_list)
            prime_numbers_list.append(current_number)
            prime_positions_dict[(row_number, column_number)] = prime_index
            row_of_each_prime_list.append(row_number)
    number_of_primes = len(prime_numbers_list)
    parent_array = list(range(number_of_primes))
    row_column_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for position, current_prime_index in prime_positions_dict.items():
        row_number, column_number = position
        for delta_row, delta_column in row_column_deltas:
            new_row_number = row_number + delta_row
            new_column_number = column_number + delta_column
            if 1 <= new_column_number <= new_row_number:
                new_position = (new_row_number, new_column_number)
                if new_position in prime_positions_dict:
                    union_sets(parent_array, current_prime_index, prime_positions_dict[new_position])
    component_sizes_dict = defaultdict(int)
    for prime_index in range(number_of_primes):
        root_parent = find_parent(parent_array, prime_index)
        component_sizes_dict[root_parent] += 1
    total_sum_for_row = 0
    for prime_index in range(number_of_primes):
        if row_of_each_prime_list[prime_index] == target_row:
            root_parent = find_parent(parent_array, prime_index)
            if component_sizes_dict[root_parent] >= 3:
                total_sum_for_row += prime_numbers_list[prime_index]
    return total_sum_for_row

if __name__ == '__main__':
    rows_to_compute = [5678027, 7208785]
    with multiprocessing.Pool(processes=2) as pool:
        results_list = pool.map(compute_s_for_row, rows_to_compute)
    final_answer = sum(results_list)
    print(final_answer)