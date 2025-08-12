# Problem: https://projecteuler.net/problem=156
from math import log10


def count_digit_up_to(limit_value, target_digit):
    if limit_value <= 0:
        return 0

    total_count = 0
    position_multiplier = 1
    digit_char = str(target_digit)

    while position_multiplier <= limit_value:
        higher = limit_value // (position_multiplier * 10)
        current = (limit_value // position_multiplier) % 10
        lower = limit_value % position_multiplier

        if target_digit != 0:
            total_count += higher * position_multiplier
        else:
            if higher != 0:
                total_count += (higher - 1) * position_multiplier

        if current > target_digit:
            total_count += position_multiplier
        elif current == target_digit:
            total_count += lower + 1

        position_multiplier *= 10

    if target_digit == 0:
        total_count -= 1

    return total_count


def compute_g_value(n_value, target_digit):
    return count_digit_up_to(n_value, target_digit) - n_value


def can_contain_zero(g_start, interval_length, max_digits):
    max_increase_per_step = max_digits - 1
    min_possible = g_start - interval_length
    max_possible = g_start + interval_length * max_increase_per_step
    return min_possible <= 0 <= max_possible


def search_solutions_in_range(start_value, end_value, target_digit, max_digits, solutions_list):
    g_start = compute_g_value(start_value, target_digit)
    g_end = compute_g_value(end_value, target_digit)

    if g_start == 0:
        solutions_list.append(start_value)
    if end_value != start_value and g_end == 0:
        solutions_list.append(end_value)

    interval_length = end_value - start_value

    if interval_length <= 1:
        return

    if not can_contain_zero(g_start, interval_length, max_digits) and not can_contain_zero(g_end, interval_length, max_digits):
        return

    middle_value = (start_value + end_value) // 2
    if middle_value == start_value or middle_value == end_value:
        return

    search_solutions_in_range(start_value, middle_value, target_digit, max_digits, solutions_list)
    search_solutions_in_range(middle_value, end_value, target_digit, max_digits, solutions_list)


def solve():
    upper_limit = 10 ** 13
    max_digits = int(log10(upper_limit)) + 1

    all_solutions_sum = 0

    for digit in range(1, 10):
        solutions_for_digit = []
        search_solutions_in_range(1, upper_limit, digit, max_digits, solutions_for_digit)
        unique_solutions = sorted(set(solutions_for_digit))
        all_solutions_sum += sum(unique_solutions)

    print(all_solutions_sum)


if __name__ == "__main__":
    solve()
