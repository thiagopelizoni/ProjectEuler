# Problem: https://projecteuler.net/problem=215
import numpy as np
from tqdm import tqdm

wall_width = 32
wall_height = 10

def generate_wall_row_configurations(width):
    configurations = []
    stack = [(0, 0)]
    while stack:
        current_position, current_mask = stack.pop()
        if current_position == width:
            configurations.append(current_mask)
            continue
        for tile_length in [3, 2]:
            new_position = current_position + tile_length
            if new_position > width:
                continue
            new_mask = current_mask
            if current_position > 0:
                new_mask |= (1 << (current_position - 1))
            stack.append((new_position, new_mask))
    return configurations

def compute_transition_matrix_row(state_index, all_states_list):
    my_state_mask = all_states_list[state_index]
    row_data = np.zeros(len(all_states_list), dtype=np.float64)
    for target_state_index, target_state_mask in enumerate(all_states_list):
        if (my_state_mask & target_state_mask) == 0:
            row_data[target_state_index] = 1.0
    return row_data

states_list = generate_wall_row_configurations(wall_width)
number_of_states = len(states_list)

transition_matrix_rows = []
for state_index in tqdm(range(number_of_states)):
    transition_matrix_rows.append(compute_transition_matrix_row(state_index, states_list))

transition_matrix = np.vstack(transition_matrix_rows)

initial_ways_vector = np.ones(number_of_states, dtype=np.float64)

current_ways_vector = initial_ways_vector
for layer in range(wall_height - 1):
    current_ways_vector = np.dot(current_ways_vector, transition_matrix)

total_number_of_ways = np.sum(current_ways_vector)

print(int(total_number_of_ways))