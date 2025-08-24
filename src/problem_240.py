# Problem: https://projecteuler.net/problem=240
import math
from tqdm import tqdm


def compute_ways_for_offsets(variable_count, max_offset, target_sum):
    if target_sum < 0:
        return 0
    if variable_count == 0:
        return 1 if target_sum == 0 else 0

    ways_for_sum = [0] * (target_sum + 1)
    ways_for_sum[0] = 1

    for _ in range(variable_count):
        next_ways_for_sum = [0] * (target_sum + 1)
        for current_sum in range(target_sum + 1):
            count_at_sum = ways_for_sum[current_sum]
            if count_at_sum == 0:
                continue
            for offset in range(max_offset + 1):
                new_sum = current_sum + offset
                if new_sum > target_sum:
                    break
                next_ways_for_sum[new_sum] += count_at_sum
        ways_for_sum = next_ways_for_sum

    return ways_for_sum[target_sum]


total_ways = 0

for base_value in tqdm(range(1, 13)):
    max_offset_for_high = 11 - base_value
    if max_offset_for_high < 0:
        continue

    for high_count in range(10):
        required_offset_sum = 70 - 10 * base_value - high_count
        if required_offset_sum < 0:
            continue
        if required_offset_sum > high_count * (max_offset_for_high + 1):
            continue

        ways_high_group = compute_ways_for_offsets(high_count, max_offset_for_high, required_offset_sum)
        if ways_high_group == 0:
            continue

        choose_high_positions = math.comb(20, high_count)
        remaining_positions = 20 - high_count
        min_equal_count = 10 - high_count

        for equal_count in range(min_equal_count, remaining_positions + 1):
            choose_equal_positions = math.comb(remaining_positions, equal_count)
            low_count = remaining_positions - equal_count
            ways_low_group = pow(base_value - 1, low_count)
            total_ways += (
                choose_high_positions
                * ways_high_group
                * choose_equal_positions
                * ways_low_group
            )

print(total_ways)