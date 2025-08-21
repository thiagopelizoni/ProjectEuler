# Problem: https://projecteuler.net/problem=220
from tqdm import tqdm


DIRECTION_X = [0, 1, 0, -1]
DIRECTION_Y = [1, 0, -1, 0]


steps_per_block = {'a': [0] * 51, 'b': [0] * 51}
offset_x_per_block = {'a': [[0] * 4 for _ in range(51)], 'b': [[0] * 4 for _ in range(51)]}
offset_y_per_block = {'a': [[0] * 4 for _ in range(51)], 'b': [[0] * 4 for _ in range(51)]}
final_direction_per_block = {'a': [[0] * 4 for _ in range(51)], 'b': [[0] * 4 for _ in range(51)]}


for block_kind in ('a', 'b'):
    for direction_index in range(4):
        final_direction_per_block[block_kind][0][direction_index] = direction_index


for depth in tqdm(range(1, 51)):
    for block_kind in ('a', 'b'):
        for start_direction in range(4):
            x = 0
            y = 0
            current_direction = start_direction
            sub_depth = depth - 1

            if block_kind == 'a':
                x += offset_x_per_block['a'][sub_depth][current_direction]
                y += offset_y_per_block['a'][sub_depth][current_direction]
                current_direction = final_direction_per_block['a'][sub_depth][current_direction]

                current_direction = (current_direction + 1) % 4
                x += offset_x_per_block['b'][sub_depth][current_direction]
                y += offset_y_per_block['b'][sub_depth][current_direction]
                current_direction = final_direction_per_block['b'][sub_depth][current_direction]

                x += DIRECTION_X[current_direction]
                y += DIRECTION_Y[current_direction]
                current_direction = (current_direction + 1) % 4
            else:
                current_direction = (current_direction - 1) % 4
                x += DIRECTION_X[current_direction]
                y += DIRECTION_Y[current_direction]

                x += offset_x_per_block['a'][sub_depth][current_direction]
                y += offset_y_per_block['a'][sub_depth][current_direction]
                current_direction = final_direction_per_block['a'][sub_depth][current_direction]

                current_direction = (current_direction - 1) % 4
                x += offset_x_per_block['b'][sub_depth][current_direction]
                y += offset_y_per_block['b'][sub_depth][current_direction]
                current_direction = final_direction_per_block['b'][sub_depth][current_direction]

            offset_x_per_block[block_kind][depth][start_direction] = x
            offset_y_per_block[block_kind][depth][start_direction] = y
            final_direction_per_block[block_kind][depth][start_direction] = current_direction

        steps_per_block[block_kind][depth] = (1 << depth) - 1


def process_block(block_type, depth, position_x, position_y, direction, remaining_steps):
    if remaining_steps <= 0:
        return position_x, position_y, direction, remaining_steps

    if block_type in 'FLR':
        if block_type == 'F':
            position_x += DIRECTION_X[direction]
            position_y += DIRECTION_Y[direction]
            remaining_steps -= 1
        elif block_type == 'L':
            direction = (direction - 1) % 4
        elif block_type == 'R':
            direction = (direction + 1) % 4

        return position_x, position_y, direction, remaining_steps

    if depth == 0:
        return position_x, position_y, direction, remaining_steps

    steps_in_this_block = steps_per_block[block_type][depth]

    if steps_in_this_block <= remaining_steps:
        position_x += offset_x_per_block[block_type][depth][direction]
        position_y += offset_y_per_block[block_type][depth][direction]
        direction = final_direction_per_block[block_type][depth][direction]
        remaining_steps -= steps_in_this_block
        return position_x, position_y, direction, remaining_steps

    if block_type == 'a':
        sequence = [('a', depth - 1), ('R', 0), ('b', depth - 1), ('F', 0), ('R', 0)]
    else:
        sequence = [('L', 0), ('F', 0), ('a', depth - 1), ('L', 0), ('b', depth - 1)]

    for sub_block_type, sub_depth in sequence:
        position_x, position_y, direction, remaining_steps = process_block(
            sub_block_type, sub_depth, position_x, position_y, direction, remaining_steps
        )
        if remaining_steps <= 0:
            break

    return position_x, position_y, direction, remaining_steps


position_x = 0
position_y = 0
direction = 0
steps_to_take = 1_000_000_000_000

position_x, position_y, direction, steps_to_take = process_block(
    'F', 0, position_x, position_y, direction, steps_to_take
)

position_x, position_y, direction, steps_to_take = process_block(
    'a', 50, position_x, position_y, direction, steps_to_take
)

print(f"{position_x},{position_y}")