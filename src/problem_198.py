# Problem: https://projecteuler.net/problem=198
from tqdm import tqdm
import math

def compute_ambiguous_numbers(max_denominator=10**8, upper_bound_fraction=100):
    half_max_denominator = max_denominator // 2
    sqrt_half_max = int(math.sqrt(half_max_denominator))
    current_left_denominator = sqrt_half_max
    stack_of_denominators = list(range(upper_bound_fraction, sqrt_half_max))
    ambiguous_count = 0
    progress_bar = tqdm(desc="Processing Farey intervals")
    while stack_of_denominators:
        current_right_denominator = stack_of_denominators[-1]
        if current_left_denominator * current_right_denominator > half_max_denominator:
            current_left_denominator = stack_of_denominators.pop()
        else:
            ambiguous_count += 1
            stack_of_denominators.append(current_left_denominator + current_right_denominator)
        progress_bar.update(1)
    progress_bar.close()
    adjustment_value = half_max_denominator - (upper_bound_fraction // 2)
    total_ambiguous_numbers = ambiguous_count + adjustment_value
    return total_ambiguous_numbers

if __name__ == "__main__":
    result = compute_ambiguous_numbers()
    print(result)