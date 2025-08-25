# Problem: https://projecteuler.net/problem=249
import os
import numpy as np
from numba import njit
from sympy import primerange
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed


def generate_is_prime(upper_limit):
    is_prime_sieve = np.ones(upper_limit + 1, dtype=bool)
    is_prime_sieve[0] = False
    is_prime_sieve[1] = False
    for number in range(2, int(upper_limit**0.5) + 1):
        if is_prime_sieve[number]:
            is_prime_sieve[number * number :: number] = False
    return is_prime_sieve


@njit
def update_dp_array(subset_sum_counts, prime, max_sum, modulus_value):
    for current_sum in range(max_sum, prime - 1, -1):
        subset_sum_counts[current_sum] = (
            subset_sum_counts[current_sum] + subset_sum_counts[current_sum - prime]
        ) % modulus_value


def compute_subset_count_chunk(start_sum, end_sum, subset_sum_counts, is_prime_sieve, modulus_value):
    chunk_prime_sum_count = 0
    for current_sum in range(start_sum, end_sum):
        if is_prime_sieve[current_sum]:
            chunk_prime_sum_count = (
                chunk_prime_sum_count + subset_sum_counts[current_sum]
            ) % modulus_value
    return chunk_prime_sum_count


def main():
    primes_under_5000 = list(primerange(2, 5000))
    max_possible_sum = sum(primes_under_5000)
    modulus_value = 10**16

    subset_sum_counts = np.zeros(max_possible_sum + 1, dtype=np.uint64)
    subset_sum_counts[0] = 1

    for prime in tqdm(primes_under_5000, desc="Calculating subset sums"):
        update_dp_array(subset_sum_counts, prime, max_possible_sum, modulus_value)

    is_prime_sieve = generate_is_prime(max_possible_sum)

    number_of_processes = os.cpu_count()
    chunk_size = (max_possible_sum + 1) // number_of_processes

    tasks = []
    with ProcessPoolExecutor() as executor:
        for i in range(number_of_processes):
            start_sum = i * chunk_size
            end_sum = (
                start_sum + chunk_size
                if i < number_of_processes - 1
                else max_possible_sum + 1
            )
            tasks.append(
                executor.submit(
                    compute_subset_count_chunk,
                    start_sum,
                    end_sum,
                    subset_sum_counts,
                    is_prime_sieve,
                    modulus_value,
                )
            )

    total_prime_subset_sums = 0
    progress_bar = tqdm(
        as_completed(tasks), total=len(tasks), desc="Summing results"
    )
    for future in progress_bar:
        total_prime_subset_sums = (
            total_prime_subset_sums + future.result()
        ) % modulus_value

    print(total_prime_subset_sums)


if __name__ == "__main__":
    main()