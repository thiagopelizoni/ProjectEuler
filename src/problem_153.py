# Problem: https://projecteuler.net/problem=153
import math
import numpy as np
from math import gcd, isqrt
from tqdm import tqdm

upper_limit = 10**8

divisor_sums_array = np.zeros(upper_limit + 1, dtype=np.int64)

for current_divisor in range(1, upper_limit + 1):
    divisor_sums_array[current_divisor::current_divisor] += current_divisor

cumulative_divisor_sums_array = np.cumsum(divisor_sums_array)

grand_total = 0

max_root_value = isqrt(upper_limit)

for primitive_real_part in tqdm(range(1, max_root_value + 1)):
    remaining_for_imag = upper_limit - primitive_real_part ** 2

    if remaining_for_imag < 0:
        continue

    max_primitive_imag_part = isqrt(remaining_for_imag)

    for primitive_imag_part in range(0, max_primitive_imag_part + 1):

        if gcd(primitive_real_part, primitive_imag_part) != 1:
            continue

        primitive_norm_value = primitive_real_part ** 2 + primitive_imag_part ** 2

        if primitive_norm_value == 0:
            continue

        current_quotient_value = upper_limit // primitive_norm_value

        current_contribution = primitive_real_part * cumulative_divisor_sums_array[current_quotient_value]

        if primitive_imag_part == 0:
            grand_total += current_contribution

        else:
            grand_total += 2 * current_contribution

print(grand_total)