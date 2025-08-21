# Problem: https://projecteuler.net/problem=227
import numpy as np
from tqdm import tqdm


number_of_players = 100
maximum_separation = number_of_players // 2

relative_move_probabilities = {
    -2: 1 / 36,
    -1: 8 / 36,
    0: 18 / 36,
    1: 8 / 36,
    2: 1 / 36,
}

number_of_states = maximum_separation
transition_matrix = np.eye(number_of_states, dtype=float)
right_hand_side = np.ones(number_of_states, dtype=float)

for separation in tqdm(range(1, number_of_states + 1), desc="building matrix"):
    row_index = separation - 1

    for relative_move, probability in relative_move_probabilities.items():
        new_difference = (separation + relative_move) % number_of_players
        new_separation = min(new_difference, number_of_players - new_difference)

        if new_separation != 0:
            column_index = new_separation - 1
            transition_matrix[row_index, column_index] -= probability

expected_turns_per_state = np.linalg.solve(transition_matrix, right_hand_side)

initial_separation = maximum_separation
expected_number_of_turns = expected_turns_per_state[initial_separation - 1]

print(f"{expected_number_of_turns:.10g}")