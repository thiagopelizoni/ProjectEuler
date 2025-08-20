# Problem: https://projecteuler.net/problem=214
import numpy as np
from tqdm import tqdm

max_limit = 40000000

phi_values = np.arange(max_limit + 1, dtype=np.int64)

primes_list = []

for current_number in tqdm(range(2, max_limit + 1)):
    if phi_values[current_number] == current_number:
        primes_list.append(current_number)
        for multiple in range(current_number, max_limit + 1, current_number):
            phi_values[multiple] = (phi_values[multiple] // current_number) * (current_number - 1)

chain_lengths = np.zeros(max_limit + 1, dtype=np.int64)

chain_lengths[1] = 1

for current_number in tqdm(range(2, max_limit + 1)):
    chain_lengths[current_number] = 1 + chain_lengths[phi_values[current_number]]

sum_of_qualifying_primes = 0

for prime in primes_list:
    if chain_lengths[prime] == 25:
        sum_of_qualifying_primes += prime

print(sum_of_qualifying_primes)