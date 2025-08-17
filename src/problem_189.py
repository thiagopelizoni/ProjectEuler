# Problem: https://projecteuler.net/problem=189
from tqdm import tqdm

height_of_grid = 8
number_of_colors = 3
triangles_color_list = [0] * (height_of_grid * height_of_grid)
cache_dict = {}

progress_bar = tqdm(total=height_of_grid - 1, desc="Processing rows", unit=" row")

def compute_id_for_row(current_row):
    starting_index = current_row * current_row
    row_width = 2 * current_row + 1
    hash_result = current_row
    for triangle_index in range(starting_index + 2, starting_index + row_width, 2):
        color_difference = triangles_color_list[triangle_index - 2] - triangles_color_list[triangle_index]
        if color_difference < 0:
            color_difference += number_of_colors

        hash_result = hash_result * number_of_colors + color_difference
    reverse_hash = current_row
    for triangle_index in range(starting_index + row_width - 1, starting_index + 1, -2):
        color_difference = triangles_color_list[triangle_index - 2] - triangles_color_list[triangle_index]
        if color_difference < 0:
            color_difference += number_of_colors

        reverse_hash = reverse_hash * number_of_colors + color_difference
    if hash_result > reverse_hash:
        hash_result = reverse_hash

    return hash_result

def recursive_search(current_row=0, current_column=0):
    starting_index = current_row * current_row
    current_index = starting_index + current_column
    row_width = 2 * current_row + 1
    next_row_to_process = current_row
    next_column_to_process = current_column + 1
    if next_column_to_process == row_width:
        next_row_to_process += 1
        next_column_to_process = 0

    previous_row_id = 0
    if current_column == 0:
        if current_row == height_of_grid:
            return 1

        if current_row > 0:
            previous_row_id = compute_id_for_row(current_row - 1)
            if previous_row_id in cache_dict:
                return cache_dict[previous_row_id]

            progress_bar.update(1)
    total_ways = 0
    if current_column % 2 == 0:
        for color_choice in range(1, number_of_colors + 1):
            if current_column > 0 and triangles_color_list[current_index - 1] == color_choice:
                continue

            triangles_color_list[current_index] = color_choice
            total_ways += recursive_search(next_row_to_process, next_column_to_process)
    else:
        for color_choice in range(1, number_of_colors + 1):
            if triangles_color_list[current_index - 1] == color_choice or triangles_color_list[current_index - 2 * current_row] == color_choice:
                continue

            triangles_color_list[current_index] = color_choice
            total_ways += recursive_search(next_row_to_process, next_column_to_process)
    if current_column == 0 and current_row > 0:
        cache_dict[previous_row_id] = total_ways

    return total_ways

final_result = recursive_search()
print(final_result)
progress_bar.close()