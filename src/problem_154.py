# Problem: https://projecteuler.net/problem=154
import numpy as np
import numba as nb
from tqdm import tqdm

total_layer_size = 200000
first_prime = 2
required_exponent_first = 12
second_prime = 5
required_exponent_second = 12

valuation_per_number_first_prime = np.zeros(total_layer_size + 1, dtype=np.uint32)
valuation_per_number_second_prime = np.zeros(total_layer_size + 1, dtype=np.uint32)

for current_number in range(1, total_layer_size + 1):
    temporary_number = current_number
    exponent_count = 0
    while temporary_number % first_prime == 0:
        temporary_number //= first_prime
        exponent_count += 1
    valuation_per_number_first_prime[current_number] = exponent_count

    temporary_number = current_number
    exponent_count = 0
    while temporary_number % second_prime == 0:
        temporary_number //= second_prime
        exponent_count += 1
    valuation_per_number_second_prime[current_number] = exponent_count

cumulative_valuation_first_prime = np.cumsum(valuation_per_number_first_prime, dtype=np.uint64)
cumulative_valuation_second_prime = np.cumsum(valuation_per_number_second_prime, dtype=np.uint64)

@nb.njit
def calculate_count_for_layer(layer_index, cumulative_first, cumulative_second, req_first, req_second):
    outer_exponent_first = cumulative_first[total_layer_size] - cumulative_first[layer_index] - cumulative_first[total_layer_size - layer_index]
    outer_exponent_second = cumulative_second[total_layer_size] - cumulative_second[layer_index] - cumulative_second[total_layer_size - layer_index]

    if outer_exponent_first >= req_first and outer_exponent_second >= req_second:
        return layer_index + 1

    layer_contribution_count = 0
    maximum_inner_index = layer_index // 2 + 1

    for inner_index in range(maximum_inner_index):
        inner_exponent_first = cumulative_first[layer_index] - cumulative_first[inner_index] - cumulative_first[layer_index - inner_index]
        inner_exponent_second = cumulative_second[layer_index] - cumulative_second[inner_index] - cumulative_second[layer_index - inner_index]

        if (outer_exponent_first + inner_exponent_first >= req_first) and (outer_exponent_second + inner_exponent_second >= req_second):
            layer_contribution_count += 1
            if inner_index < layer_index - inner_index:
                layer_contribution_count += 1

    return layer_contribution_count

overall_total_count = 0
half_layer_size = total_layer_size // 2

for current_layer_index in tqdm(range(half_layer_size + 1)):
    current_count = calculate_count_for_layer(current_layer_index, cumulative_valuation_first_prime, cumulative_valuation_second_prime, required_exponent_first, required_exponent_second)
    symmetric_layer_index = total_layer_size - current_layer_index
    if current_layer_index == symmetric_layer_index:
        overall_total_count += current_count
    else:
        symmetric_count = calculate_count_for_layer(symmetric_layer_index, cumulative_valuation_first_prime, cumulative_valuation_second_prime, required_exponent_first, required_exponent_second)
        overall_total_count += current_count + symmetric_count

print(overall_total_count)