# Problem: https://projecteuler.net/problem=147
from functools import lru_cache


@lru_cache(maxsize=None)
def rectangles(grid_width, grid_height):
    if grid_width == 1 and grid_height == 1:
        return 1

    if grid_width < grid_height:
        return rectangles(grid_height, grid_width)

    new_rectangles = sum(range(1, grid_height + 1))
    new_rectangles *= grid_width

    for index in range(1, grid_height + 1):
        height_part = index
        width_part = grid_height * 2 - height_part
        base_area = width_part * height_part - (0 if grid_width > grid_height else (height_part % 2))
        if width_part == height_part:
            new_rectangles += base_area
        else:
            new_rectangles += base_area * 2

    return new_rectangles + rectangles(grid_width - 1, grid_height)


def total_rectangles(max_width, max_height):
    total_value = 0

    for current_width in range(1, max_width + 1):
        for current_height in range(1, max_height + 1):
            total_value += rectangles(current_width, current_height)

    return total_value


def main():
    result_value = total_rectangles(47, 43)
    print(result_value)


if __name__ == "__main__":
    main()
