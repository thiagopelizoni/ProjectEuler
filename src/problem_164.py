# Problem: https://projecteuler.net/problem=164
import numpy as np

def count_valid_numbers(total_digits: int) -> int:
    last_two_counts = np.zeros((10, 10), dtype=object)

    for first_digit in range(1, 10):
        for second_digit in range(10):
            if first_digit + second_digit <= 9:
                last_two_counts[first_digit, second_digit] += 1

    for current_length in range(2, total_digits):
        new_counts = np.zeros((10, 10), dtype=object)
        for prev_a in range(10):
            for prev_b in range(10):
                current_count = last_two_counts[prev_a, prev_b]
                if current_count:
                    max_next = 9 - (prev_a + prev_b)
                    if max_next >= 0:
                        for next_digit in range(max_next + 1):
                            new_counts[prev_b, next_digit] += current_count
        last_two_counts = new_counts

    total_count = int(np.sum(last_two_counts))
    return total_count

if __name__ == "__main__":
    print(count_valid_numbers(20))
