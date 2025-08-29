# Problem: https://projecteuler.net/problem=259
import os
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from tqdm import tqdm


def compute_combinations(arguments):
    left_values_set, right_values_set = arguments
    combination_results = set()

    for left_value in left_values_set:
        for right_value in right_values_set:
            combination_results.add(left_value + right_value)
            combination_results.add(left_value - right_value)
            combination_results.add(left_value * right_value)

            if right_value != 0:
                combination_results.add(left_value / right_value)

    return combination_results


def get_cpu_count():
    try:
        return os.cpu_count() or 1
    except (NotImplementedError, AttributeError):
        return 1


def solve_euler_259():
    digits_sequence = "123456789"
    sequence_length = len(digits_sequence)

    reachable_values = [
        [set() for _ in range(sequence_length)]
        for _ in range(sequence_length)
    ]

    for i in range(sequence_length):
        for j in range(i, sequence_length):
            concatenated_number_str = digits_sequence[i : j + 1]
            value = Fraction(int(concatenated_number_str))
            reachable_values[i][j].add(value)

    cpu_count = get_cpu_count()

    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        progress_bar = tqdm(
            range(2, sequence_length + 1),
            desc="Calculating reachable numbers"
        )

        for length in progress_bar:
            tasks_arguments = []
            tasks_metadata = []

            for start_index in range(sequence_length - length + 1):
                end_index = start_index + length - 1

                for split_index in range(start_index, end_index):
                    left_part_values = reachable_values[start_index][split_index]
                    right_part_values = (
                        reachable_values[split_index + 1][end_index]
                    )

                    tasks_arguments.append((left_part_values, right_part_values))
                    tasks_metadata.append((start_index, end_index))

            if tasks_arguments:
                results_iterator = executor.map(
                    compute_combinations, tasks_arguments
                )

                for task_index, combinations in enumerate(results_iterator):
                    start_index, end_index = tasks_metadata[task_index]
                    reachable_values[start_index][end_index].update(combinations)

    final_reachable_values = reachable_values[0][sequence_length - 1]

    sum_of_positive_integers = 0
    for value in final_reachable_values:
        if value > 0 and value.denominator == 1:
            sum_of_positive_integers += value.numerator

    return sum_of_positive_integers


if __name__ == "__main__":
    result = solve_euler_259()
    print(result)