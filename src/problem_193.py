# Problem: https://projecteuler.net/problem=193
import math
import os
from multiprocessing import Pool
from tqdm import tqdm
import array

def create_mobius_sieve(maximum_d_value):
    mobius_array = array.array('b', [0] * (maximum_d_value + 1))
    mobius_array[1] = 1
    visited_flags = [False] * (maximum_d_value + 1)
    prime_numbers = []
    for current_number in tqdm(range(2, maximum_d_value + 1), desc="Building Mobius sieve"):
        if not visited_flags[current_number]:
            prime_numbers.append(current_number)
            mobius_array[current_number] = -1
        for prime_index, current_prime in enumerate(prime_numbers):
            if current_number * current_prime > maximum_d_value:
                break
            visited_flags[current_number * current_prime] = True
            if current_number % current_prime == 0:
                mobius_array[current_number * current_prime] = 0
                break
            else:
                mobius_array[current_number * current_prime] = -mobius_array[current_number]
    return mobius_array

def calculate_partial_squarefree_count(arguments):
    mobius_array, start_d, end_d, upper_limit_minus_one = arguments
    local_count = 0
    for current_d in range(start_d, end_d + 1):
        mobius_value = mobius_array[current_d]
        if mobius_value != 0:
            square_d = current_d * current_d
            local_count += mobius_value * (upper_limit_minus_one // square_d)
    return local_count

upper_limit = 1 << 50
upper_limit_minus_one = upper_limit - 1
maximum_d_value = math.isqrt(upper_limit_minus_one)

print("Starting Mobius function computation...")
mobius_array = create_mobius_sieve(maximum_d_value)
print("Mobius function ready. Starting count computation...")

number_of_processes = os.cpu_count()
chunk_size_per_process = (maximum_d_value + number_of_processes - 1) // number_of_processes
task_chunks = []
for process_index in range(number_of_processes):
    start_d = process_index * chunk_size_per_process + 1
    end_d = min((process_index + 1) * chunk_size_per_process, maximum_d_value)
    if start_d <= end_d:
        task_chunks.append((mobius_array, start_d, end_d, upper_limit_minus_one))

with Pool(number_of_processes) as process_pool:
    partial_counts = list(tqdm(process_pool.imap_unordered(calculate_partial_squarefree_count, task_chunks),
                               total=len(task_chunks), desc="Computing partial counts"))

total_squarefree_numbers = sum(partial_counts)
print(total_squarefree_numbers)