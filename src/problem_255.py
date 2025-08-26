# Problem: https://projecteuler.net/problem=255
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from decimal import Decimal


def compute_iterations_sum(
    subrange_min_number,
    subrange_max_number,
    current_guess,
    current_iteration_count
):
    total_iterations_in_subrange = 0

    if subrange_min_number > subrange_max_number:
        return 0

    min_ceiling_of_division = (subrange_min_number + current_guess - 1) // current_guess
    max_ceiling_of_division = (subrange_max_number + current_guess - 1) // current_guess

    for ceiling_of_division in range(min_ceiling_of_division, max_ceiling_of_division + 1):
        new_subrange_min_number = max(subrange_min_number, (ceiling_of_division - 1) * current_guess + 1)
        new_subrange_max_number = min(subrange_max_number, ceiling_of_division * current_guess)

        if new_subrange_min_number > new_subrange_max_number:
            continue

        next_guess = (current_guess + ceiling_of_division) // 2
        next_iteration_count = current_iteration_count + 1
        new_subrange_size = new_subrange_max_number - new_subrange_min_number + 1

        if next_guess == current_guess:
            total_iterations_in_subrange += new_subrange_size * next_iteration_count
        else:
            total_iterations_in_subrange += compute_iterations_sum(
                new_subrange_min_number,
                new_subrange_max_number,
                next_guess,
                next_iteration_count
            )

    return total_iterations_in_subrange


def compute_for_pair(
    pair_min_divisor_value,
    initial_guess,
    overall_min_number,
    overall_max_number
):
    pair_min_number = max(overall_min_number, (pair_min_divisor_value - 1) * initial_guess + 1)
    pair_max_number = min(overall_max_number, (pair_min_divisor_value + 1) * initial_guess)

    if pair_min_number > pair_max_number:
        return 0

    next_guess = (initial_guess + pair_min_divisor_value) // 2
    next_iteration_count = 1
    size_of_pair_range = pair_max_number - pair_min_number + 1

    if next_guess == initial_guess:
        return size_of_pair_range * next_iteration_count
    else:
        return compute_iterations_sum(
            pair_min_number,
            pair_max_number,
            next_guess,
            next_iteration_count
        )


def compute_for_chunk(
    chunk_min_divisor_value,
    chunk_max_divisor_value,
    divisor_step_value,
    initial_guess,
    overall_min_number,
    overall_max_number
):
    total_iterations_in_chunk = 0

    for divisor_value in range(chunk_min_divisor_value, chunk_max_divisor_value + 1, divisor_step_value):
        total_iterations_in_chunk += compute_for_pair(
            divisor_value,
            initial_guess,
            overall_min_number,
            overall_max_number
        )

    return total_iterations_in_chunk


if __name__ == '__main__':
    LOWER_BOUND = 10 ** 13
    UPPER_BOUND = 10 ** 14 - 1
    INITIAL_GUESS = 7 * 10 ** 6
    DIVISOR_STEP = 2
    CHUNKS_PER_CPU = 10

    min_divisor_value = (LOWER_BOUND + INITIAL_GUESS - 1) // INITIAL_GUESS
    max_divisor_value = (UPPER_BOUND + INITIAL_GUESS - 1) // INITIAL_GUESS

    chunk_processing_min_divisor = min_divisor_value
    chunk_processing_max_divisor = max_divisor_value - 1 if max_divisor_value % 2 == 1 else max_divisor_value

    total_number_of_pairs = ((chunk_processing_max_divisor - chunk_processing_min_divisor) // DIVISOR_STEP) + 1

    cpu_core_count = os.cpu_count()
    total_number_of_chunks = cpu_core_count * CHUNKS_PER_CPU
    number_of_pairs_per_chunk = (total_number_of_pairs + total_number_of_chunks - 1) // total_number_of_chunks

    total_iterations_sum = 0

    with ProcessPoolExecutor(max_workers=cpu_core_count) as pool:
        future_tasks = []
        for chunk_index in range(total_number_of_chunks):
            start_pair_index = chunk_index * number_of_pairs_per_chunk
            end_pair_index = min((chunk_index + 1) * number_of_pairs_per_chunk - 1, total_number_of_pairs - 1)

            if start_pair_index > end_pair_index:
                continue

            chunk_start_divisor_value = chunk_processing_min_divisor + start_pair_index * DIVISOR_STEP
            chunk_end_divisor_value = chunk_processing_min_divisor + end_pair_index * DIVISOR_STEP

            task = pool.submit(
                compute_for_chunk,
                chunk_start_divisor_value,
                chunk_end_divisor_value,
                DIVISOR_STEP,
                INITIAL_GUESS,
                LOWER_BOUND,
                UPPER_BOUND
            )
            future_tasks.append(task)

        progress_bar = tqdm(as_completed(future_tasks), total=len(future_tasks))
        for future in progress_bar:
            total_iterations_sum += future.result()

    total_numbers_in_range = UPPER_BOUND - LOWER_BOUND + 1
    average_iterations_result = Decimal(total_iterations_sum) / Decimal(total_numbers_in_range)

    print(f'{average_iterations_result:.10f}')