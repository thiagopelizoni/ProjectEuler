# Problem: https://projecteuler.net/problem=150
import numpy as np


def generate_triangle(total_rows):
    total_values = total_rows * (total_rows + 1) // 2
    sequence = np.empty(total_values, dtype=np.int64)

    modulus = 1 << 20
    offset = 1 << 19

    t_value = 0
    for index in range(total_values):
        t_value = (615949 * t_value + 797807) % modulus
        sequence[index] = t_value - offset

    rows = []
    prefix_rows = []
    start_index = 0

    for row_index in range(1, total_rows + 1):
        end_index = start_index + row_index
        row_values = sequence[start_index:end_index]
        rows.append(row_values)
        prefix = np.empty(row_index + 1, dtype=np.int64)
        prefix[0] = 0
        np.cumsum(row_values, dtype=np.int64, out=prefix[1:])
        prefix_rows.append(prefix)
        start_index = end_index

    return rows, prefix_rows


def minimal_subtriangle_sum(total_rows):
    rows, prefix_rows = generate_triangle(total_rows)
    minimal_value = None

    for top_row in range(total_rows):
        start_count = top_row + 1
        current_sums = np.zeros(start_count, dtype=np.int64)

        for bottom_row in range(top_row, total_rows):
            segment_length = bottom_row - top_row + 1
            prefix = prefix_rows[bottom_row]
            segment_sums = prefix[segment_length:segment_length + start_count] - prefix[:start_count]
            current_sums += segment_sums
            current_min = int(current_sums.min())

            if minimal_value is None or current_min < minimal_value:
                minimal_value = current_min

    return minimal_value


def main():
    total_rows = 1000
    result_value = minimal_subtriangle_sum(total_rows)
    print(result_value)


if __name__ == "__main__":
    main()
