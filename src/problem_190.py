# Problem: https://projecteuler.net/problem=190
import math
from tqdm import tqdm

maximum_m_value = 15
minimum_m_value = 2
number_of_colors = 3
total_sum_of_floor_values = 0

progress_bar = tqdm(range(minimum_m_value, maximum_m_value + 1), desc="Calculating for each m")

for current_m in progress_bar:
    exponent_sum_s = current_m * (current_m + 1) // 2
    numerator_value = pow(2, exponent_sum_s)
    for current_k in range(1, current_m + 1):
        numerator_value *= pow(current_k, current_k)

    denominator_value = pow(current_m + 1, exponent_sum_s)
    floor_of_p_m = numerator_value // denominator_value
    total_sum_of_floor_values += floor_of_p_m

print(total_sum_of_floor_values)