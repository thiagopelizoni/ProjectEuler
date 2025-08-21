# Problem: https://projecteuler.net/problem=217
import gmpy2
import multiprocessing
from tqdm import tqdm

def compute_for_length(length):
    modulus = 3 ** 15
    half_length = (length + 1) // 2
    right_half_start = length // 2 + 1
    max_possible_sum = 9 * half_length + 1

    previous_grid = [
        [
            [gmpy2.mpz(0), 0] for _ in range(max_possible_sum)
        ] for _ in range(max_possible_sum)
    ]

    previous_grid[0][0][0] = gmpy2.mpz(1)
    previous_grid[0][0][1] = 0

    for position in range(1, length + 1):
        current_grid = [
            [
                [gmpy2.mpz(0), 0] for _ in range(max_possible_sum)
            ] for _ in range(max_possible_sum)
        ]

        is_left_half = position <= half_length
        is_right_half = position >= right_half_start
        minimum_digit = 1 if position == 1 else 0

        for left_sum in range(max_possible_sum):
            for right_sum in range(max_possible_sum):
                if previous_grid[left_sum][right_sum][0] == 0:
                    continue

                previous_count = previous_grid[left_sum][right_sum][0]
                previous_sum_mod = previous_grid[left_sum][right_sum][1]

                for digit in range(minimum_digit, 10):
                    new_left_sum = left_sum + digit if is_left_half else left_sum
                    new_right_sum = right_sum + digit if is_right_half else right_sum

                    if new_left_sum >= max_possible_sum or new_right_sum >= max_possible_sum:
                        continue

                    current_grid[new_left_sum][new_right_sum][0] += previous_count
                    add_to_mod_sum = (
                        (previous_sum_mod * 10) % modulus +
                        int((digit * previous_count) % modulus)
                    ) % modulus

                    current_grid[new_left_sum][new_right_sum][1] = (
                        current_grid[new_left_sum][new_right_sum][1] + add_to_mod_sum
                    ) % modulus

        previous_grid = current_grid

    total_sum_for_length = 0

    for left_sum in range(max_possible_sum):
        for right_sum in range(max_possible_sum):
            if left_sum == right_sum:
                total_sum_for_length = (
                    total_sum_for_length + previous_grid[left_sum][right_sum][1]
                ) % modulus

    return total_sum_for_length

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        length_values = range(1, 48)
        results = list(tqdm(pool.imap(compute_for_length, length_values), total=47))

    modulus = 3 ** 15
    final_sum = sum(results) % modulus
    print(final_sum)