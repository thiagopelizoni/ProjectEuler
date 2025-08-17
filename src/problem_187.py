# Problem: https://projecteuler.net/problem=187
import math
import bisect
import numpy as np
from tqdm import tqdm

UPPER_LIMIT = 100000000

def generate_all_primes_below_given_limit(given_limit):
    square_root_of_limit = int(math.sqrt(given_limit)) + 1
    prime_check_array = np.ones(given_limit, dtype=bool)
    prime_check_array[0] = prime_check_array[1] = False
    for current_number in range(2, square_root_of_limit):
        if prime_check_array[current_number]:
            prime_check_array[current_number * current_number::current_number] = False
    all_prime_numbers = np.arange(given_limit)[prime_check_array].tolist()
    return all_prime_numbers

list_of_all_primes = generate_all_primes_below_given_limit(UPPER_LIMIT)

total_semiprime_count = 0

for prime_index in tqdm(range(len(list_of_all_primes))):
    current_prime_number = list_of_all_primes[prime_index]
    maximum_allowed_second_prime = (UPPER_LIMIT - 1) // current_prime_number
    last_valid_prime_index = bisect.bisect_right(list_of_all_primes, maximum_allowed_second_prime) - 1
    if last_valid_prime_index >= prime_index:
        total_semiprime_count += last_valid_prime_index - prime_index + 1

print(total_semiprime_count)