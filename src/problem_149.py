# Problem: https://projecteuler.net/problem=149
import numpy as np


def generate_values(total_values):
    values = np.empty(total_values, dtype=np.int64)

    k = np.arange(1, 56, dtype=np.int64)
    initial = (100003 - 200003 * k + 300007 * (k ** 3)) % 1_000_000 - 500_000
    values[:55] = initial

    for idx in range(55, total_values):
        values[idx] = (values[idx - 24] + values[idx - 55] + 1_000_000) % 1_000_000 - 500_000

    return values


def max_subarray_sum_1d(array_1d):
    cumsum = np.cumsum(array_1d, dtype=np.int64)
    prefix = np.empty_like(cumsum)
    prefix[0] = 0
    prefix[1:] = np.minimum.accumulate(cumsum[:-1])
    return int(np.max(cumsum - prefix))


def max_in_all_rows(matrix):
    best = None
    for row in matrix:
        current = max_subarray_sum_1d(row)
        if best is None or current > best:
            best = current
    return best


def max_in_all_columns(matrix):
    return max_in_all_rows(matrix.T)


def max_in_all_diagonals(matrix):
    rows, cols = matrix.shape
    best = None
    for offset in range(-rows + 1, cols):
        diag = np.diagonal(matrix, offset=offset)
        current = max_subarray_sum_1d(diag)
        if best is None or current > best:
            best = current
    return best


def max_in_all_antidiagonals(matrix):
    flipped = np.fliplr(matrix)
    return max_in_all_diagonals(flipped)


def compute_maximum_subsequence_sum():
    total_values = 2000 * 2000
    values = generate_values(total_values)
    grid = values.reshape(2000, 2000)

    best_row = max_in_all_rows(grid)
    best_col = max_in_all_columns(grid)
    best_diag = max_in_all_diagonals(grid)
    best_anti = max_in_all_antidiagonals(grid)

    return max(best_row, best_col, best_diag, best_anti)


def main():
    result_value = compute_maximum_subsequence_sum()
    print(result_value)


if __name__ == "__main__":
    main()
