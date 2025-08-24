# Problem: https://projecteuler.net/problem=244
from collections import deque
from tqdm import tqdm
import sys

MOD = 100000007

start_configuration = '.rbbrrbbrrbbrrbb'
target_configuration = '.brbbrbrrbrbbrbr'

move_directions = {
    'L': 1,
    'R': -1,
    'U': 4,
    'D': -4
}

move_values = {
    'L': 76,
    'R': 82,
    'U': 85,
    'D': 68
}

min_distances = {}
number_of_paths = {}
sum_of_checksums = {}

queue = deque()

min_distances[start_configuration] = 0
number_of_paths[start_configuration] = 1
sum_of_checksums[start_configuration] = 0

queue.append(start_configuration)

progress_bar = tqdm(desc="Processing configurations", total=None, file=sys.stdout)

while queue:
    current_configuration = queue.popleft()

    progress_bar.update(1)

    blank_position = current_configuration.index('.')

    for move_name, delta in move_directions.items():
        new_blank_position = blank_position + delta

        if not (0 <= new_blank_position < 16):
            continue

        if (delta == 1 or delta == -1) and (new_blank_position // 4 != blank_position // 4):
            continue

        new_board_list = list(current_configuration)
        new_board_list[blank_position] = new_board_list[new_blank_position]
        new_board_list[new_blank_position] = '.'
        new_configuration = ''.join(new_board_list)

        new_distance = min_distances[current_configuration] + 1

        if new_configuration not in min_distances:
            min_distances[new_configuration] = new_distance
            queue.append(new_configuration)
            number_of_paths[new_configuration] = 0
            sum_of_checksums[new_configuration] = 0

        if new_distance == min_distances[new_configuration]:
            added_paths = number_of_paths[current_configuration]
            number_of_paths[new_configuration] += added_paths

            move_value = move_values[move_name]
            added_checksum = (sum_of_checksums[current_configuration] * 243 + move_value * added_paths) % MOD
            sum_of_checksums[new_configuration] = (sum_of_checksums[new_configuration] + added_checksum) % MOD

progress_bar.close()

print(sum_of_checksums[target_configuration])