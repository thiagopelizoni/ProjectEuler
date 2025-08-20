# Problem: https://projecteuler.net/problem=213
import numpy as np
from tqdm import tqdm

grid_side_length = 30
total_cells_count = grid_side_length * grid_side_length

def calculate_index(row_position, column_position):
    return row_position * grid_side_length + column_position

transition_matrix = np.zeros((total_cells_count, total_cells_count), dtype=float)

for row_position in range(grid_side_length):
    for column_position in range(grid_side_length):
        current_index = calculate_index(row_position, column_position)

        neighbor_indices = []
        movement_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for delta_row, delta_column in movement_directions:
            new_row = row_position + delta_row
            new_column = column_position + delta_column

            if 0 <= new_row < grid_side_length and 0 <= new_column < grid_side_length:
                neighbor_indices.append(calculate_index(new_row, new_column))

        number_of_neighbors = len(neighbor_indices)

        if number_of_neighbors > 0:
            probability_each_neighbor = 1.0 / number_of_neighbors
            for neighbor_index in neighbor_indices:
                transition_matrix[current_index, neighbor_index] = probability_each_neighbor

powered_transition_matrix = np.linalg.matrix_power(transition_matrix, 50)

expected_number_of_empty_squares = 0.0

for cell_index in tqdm(range(total_cells_count)):
    probabilities_to_this_cell = powered_transition_matrix[:, cell_index]

    log_of_one_minus_probabilities = np.log1p(-probabilities_to_this_cell)
    sum_of_log_probabilities = np.sum(log_of_one_minus_probabilities)

    probability_this_cell_empty = np.exp(sum_of_log_probabilities)
    expected_number_of_empty_squares += probability_this_cell_empty

if __name__ == "__main__":
    print(round(expected_number_of_empty_squares, 6))