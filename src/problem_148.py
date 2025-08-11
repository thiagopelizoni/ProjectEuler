# Problem: https://projecteuler.net/problem=148
from functools import lru_cache


def to_base_seven(number_value):
    if number_value == 0:
        return (0,)

    digits = []

    while number_value > 0:
        digits.append(number_value % 7)
        number_value //= 7

    return tuple(reversed(digits))


@lru_cache(maxsize=None)
def sum_products_up_to_digits(digits_tuple, position_index, is_tight):
    if position_index == len(digits_tuple):
        return 1

    limit_digit = digits_tuple[position_index] if is_tight else 6
    total_sum = 0

    for chosen_digit in range(limit_digit + 1):
        next_tight = 1 if (is_tight and chosen_digit == limit_digit) else 0
        subtotal = sum_products_up_to_digits(
            digits_tuple,
            position_index + 1,
            next_tight,
        )
        total_sum += (chosen_digit + 1) * subtotal

    return total_sum


def count_not_divisible_by_seven(row_count):
    if row_count <= 0:
        return 0

    limit_digits = to_base_seven(row_count - 1)
    return sum_products_up_to_digits(limit_digits, 0, 1)


def main():
    target_rows = 10**9
    result_value = count_not_divisible_by_seven(target_rows)
    print(result_value)


if __name__ == "__main__":
    main()
