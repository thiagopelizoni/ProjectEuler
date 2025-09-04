# Problem: https://projecteuler.net/problem=255
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from decimal import Decimal
from tqdm import tqdm
from typing import Any

def compute_iterations_sum(
    range_min: int, range_max: int, current_guess: int, iteration_count: int
) -> int:
    total_iterations = 0
    if range_min > range_max:
        return 0
    min_ceil = (range_min + current_guess - 1) // current_guess
    max_ceil = (range_max + current_guess - 1) // current_guess
    for ceil_value in range(min_ceil, max_ceil + 1):
        new_min = max(range_min, (ceil_value - 1) * current_guess + 1)
        new_max = min(range_max, ceil_value * current_guess)
        if new_min > new_max:
            continue
        next_guess = (current_guess + ceil_value) // 2
        next_iteration = iteration_count + 1
        subrange_size = new_max - new_min + 1
        if next_guess == current_guess:
            total_iterations += subrange_size * next_iteration
        else:
            total_iterations += compute_iterations_sum(
                new_min, new_max, next_guess, next_iteration
            )
    return total_iterations

def compute_pair_sum(
    pair_start_ceil: int,
    initial_guess: int,
    overall_min: int,
    overall_max: int,
) -> int:
    pair_min = max(overall_min, (pair_start_ceil - 1) * initial_guess + 1)
    pair_max = min(overall_max, (pair_start_ceil + 1) * initial_guess)
    if pair_min > pair_max:
        return 0
    next_guess = (initial_guess + pair_start_ceil) // 2
    next_iteration = 1
    subrange_size = pair_max - pair_min + 1
    if next_guess == initial_guess:
        return subrange_size * next_iteration
    else:
        return compute_iterations_sum(
            pair_min, pair_max, next_guess, next_iteration
        )

def compute_chunk_sum(
    chunk_start_ceil: int,
    chunk_end_ceil: int,
    ceil_step: int,
    initial_guess: int,
    overall_min: int,
    overall_max: int,
) -> int:
    total = 0
    for ceil_value in range(chunk_start_ceil, chunk_end_ceil + 1, ceil_step):
        total += compute_pair_sum(
            ceil_value, initial_guess, overall_min, overall_max
        )
    return total

def main() -> None:
    """
    Purpose: Computes the average number of iterations required to find the rounded square root using the specified
    iterative method for all 14-digit numbers from 10^13 to 10^14 - 1.

    Args: None

    Returns: None; prints the average rounded to 10 decimal places.

    Method / Math Rationale: Recursively partitions the number range based on the ceiling of n divided by the current
    guess in the adapted Heron's method, accumulating iterations multiplied by subrange sizes when the guess
    stabilizes. Pairs consecutive initial ceiling values since they yield the same next guess due to the even initial
    guess and parity, enabling efficient counting without enumerating each number individually.

    Complexity: Time O(sqrt(U) * D) with U ≈ 10^14, D ≈ 10 average iterations, parallelized over ~10^7 pairs; space
    O(1) per process.

    References: https://projecteuler.net/problem=255
    Heron's method for square roots.
    """
    lower_bound: int = 10**13
    upper_bound: int = 10**14 - 1
    initial_guess: int = 7 * 10**6
    ceil_step: int = 2
    chunks_per_cpu: int = 10
    min_ceil: int = (lower_bound + initial_guess - 1) // initial_guess
    max_ceil: int = (upper_bound + initial_guess - 1) // initial_guess
    process_max_ceil: int = max_ceil - 1 if max_ceil % 2 == 1 else max_ceil
    num_pairs: int = ((process_max_ceil - min_ceil) // ceil_step) + 1
    cpu_count: Any = os.cpu_count()
    num_chunks: int = cpu_count * chunks_per_cpu
    pairs_per_chunk: int = (num_pairs + num_chunks - 1) // num_chunks
    total_iterations: int = 0
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        for chunk_idx in range(num_chunks):
            start_pair_idx = chunk_idx * pairs_per_chunk
            end_pair_idx = min(
                (chunk_idx + 1) * pairs_per_chunk - 1, num_pairs - 1
            )
            if start_pair_idx > end_pair_idx:
                continue
            chunk_start_ceil = min_ceil + start_pair_idx * ceil_step
            chunk_end_ceil = min_ceil + end_pair_idx * ceil_step
            future = executor.submit(
                compute_chunk_sum,
                chunk_start_ceil,
                chunk_end_ceil,
                ceil_step,
                initial_guess,
                lower_bound,
                upper_bound,
            )
            futures.append(future)
        for future in tqdm(as_completed(futures), total=len(futures)):
            total_iterations += future.result()
    num_values: int = upper_bound - lower_bound + 1
    average: Decimal = Decimal(total_iterations) / Decimal(num_values)
    print(f"{average:.10f}")

if __name__ == "__main__":
    main()