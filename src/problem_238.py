# Problem: https://projecteuler.net/problem=238
import numpy as np
from tqdm import tqdm
import numba


@numba.njit
def fill_min_p(doubled_digits, doubled_cum, L, D, min_p):
    remaining_to_set = D
    for start_index in range(L):
        current_sum = 0
        for window_length in range(1, L + 1):
            current_sum += doubled_digits[start_index + window_length - 1]
            if current_sum > D:
                break
            if current_sum > 0:
                if min_p[current_sum] > start_index + 1:
                    if min_p[current_sum] == L + 2:
                        remaining_to_set -= 1
                    min_p[current_sum] = start_index + 1
        if remaining_to_set == 0:
            break


modulus_value = 20300713
seed_value = 14025256
iterations_to_generate = 2534198

cycle_digits = []

for _ in tqdm(range(iterations_to_generate), desc="Generating digits"):
    if seed_value == 0:
        cycle_digits.append(0)
    else:
        local_digits = []
        temp_value = seed_value
        while temp_value > 0:
            local_digits.append(temp_value % 10)
            temp_value //= 10
        cycle_digits.extend(local_digits[::-1])
    seed_value = (seed_value * seed_value) % modulus_value

cycle_length = len(cycle_digits)

doubled_digits = cycle_digits + cycle_digits

cumulative_sums_doubled = np.cumsum(
    np.array([0] + doubled_digits, dtype=np.int64)
)

total_cycle_digit_sum = int(cumulative_sums_doubled[cycle_length])

min_position_for_sum = np.full(
    total_cycle_digit_sum + 1,
    cycle_length + 2,
    dtype=np.int64
)

fill_min_p(
    np.array(doubled_digits, dtype=np.int32),
    cumulative_sums_doubled,
    cycle_length,
    total_cycle_digit_sum,
    min_position_for_sum
)

target_total = 2 * 10 ** 15

total_sum_of_n = 0

for digit_sum_value in tqdm(
    range(1, total_cycle_digit_sum + 1),
    desc="Calculating total sum"
):
    if min_position_for_sum[digit_sum_value] < cycle_length + 2:
        repetitions = (target_total - digit_sum_value) // total_cycle_digit_sum + 1
        total_sum_of_n += min_position_for_sum[digit_sum_value] * repetitions

print(total_sum_of_n)