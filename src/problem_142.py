# Problem: https://projecteuler.net/problem=142
from itertools import combinations
from gmpy2 import is_square


def build_sum_of_two_squares(limit_sum):
    representation_map = {}

    max_side = int(limit_sum ** 0.5)
    for first_side in range(1, max_side + 1):
        first_square = first_side * first_side

        for second_side in range(first_side, max_side + 1):
            total_value = first_square + second_side * second_side

            if total_value > limit_sum:
                break

            if (first_side + second_side) % 2 != 0:
                continue

            if total_value not in representation_map:
                representation_map[total_value] = []

            representation_map[total_value].append((first_side, second_side))

    return representation_map


def compute_minimal_sum(limit_sum):
    representation_map = build_sum_of_two_squares(limit_sum)
    minimal_total = None

    for total_value, pairs in representation_map.items():
        if len(pairs) < 2:
            continue

        for (a_value, b_value), (c_value, d_value) in combinations(pairs, 2):
            x_value = total_value // 2

            y_value = (b_value * b_value - a_value * a_value) // 2
            z_value = (d_value * d_value - c_value * c_value) // 2

            if y_value <= 0 or z_value <= 0:
                continue

            if y_value <= z_value:
                continue

            if not is_square(y_value + z_value):
                continue

            if not is_square(y_value - z_value):
                continue

            candidate_sum = x_value + y_value + z_value

            if minimal_total is None or candidate_sum < minimal_total:
                minimal_total = candidate_sum

    return minimal_total


def main():
    search_limit = 2_500_000
    result_value = compute_minimal_sum(search_limit)
    print(result_value)


if __name__ == "__main__":
    main()
