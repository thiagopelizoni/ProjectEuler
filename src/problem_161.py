from functools import lru_cache


GRID_HEIGHT: int = 9
GRID_WIDTH: int = 12
FULL_COLUMN_MASK: int = (1 << GRID_HEIGHT) - 1


@lru_cache(maxsize=None)
def count_tilings(
    column_index: int,
    column_mask_0: int,
    column_mask_1: int,
    column_mask_2: int,
) -> int:
    if column_index == GRID_WIDTH:
        return 1 if column_mask_0 == 0 and column_mask_1 == 0 and column_mask_2 == 0 else 0

    if column_mask_0 == FULL_COLUMN_MASK:
        return count_tilings(
            column_index + 1,
            column_mask_1,
            column_mask_2,
            0,
        )

    for row_index in range(GRID_HEIGHT):
        if ((column_mask_0 >> row_index) & 1) == 0:
            first_empty_row = row_index
            break

    total_arrangements = 0

    bit_current_row = 1 << first_empty_row

    if first_empty_row + 2 < GRID_HEIGHT:
        bit_next_row = 1 << (first_empty_row + 1)
        bit_next_next_row = 1 << (first_empty_row + 2)
        vertical_mask = bit_current_row | bit_next_row | bit_next_next_row
        if column_mask_0 & vertical_mask == 0:
            total_arrangements += count_tilings(
                column_index,
                column_mask_0 | vertical_mask,
                column_mask_1,
                column_mask_2,
            )

    if column_index + 2 < GRID_WIDTH:
        if ((column_mask_1 >> first_empty_row) & 1) == 0 and ((column_mask_2 >> first_empty_row) & 1) == 0:
            total_arrangements += count_tilings(
                column_index,
                column_mask_0 | bit_current_row,
                column_mask_1 | bit_current_row,
                column_mask_2 | bit_current_row,
            )

    if column_index + 1 < GRID_WIDTH:
        if first_empty_row + 1 < GRID_HEIGHT:
            bit_next_row = 1 << (first_empty_row + 1)

            if ((column_mask_0 >> (first_empty_row + 1)) & 1) == 0 and ((column_mask_1 >> first_empty_row) & 1) == 0:
                total_arrangements += count_tilings(
                    column_index,
                    column_mask_0 | bit_current_row | bit_next_row,
                    column_mask_1 | bit_current_row,
                    column_mask_2,
                )

            if ((column_mask_0 >> (first_empty_row + 1)) & 1) == 0 and ((column_mask_1 >> (first_empty_row + 1)) & 1) == 0:
                total_arrangements += count_tilings(
                    column_index,
                    column_mask_0 | bit_current_row | bit_next_row,
                    column_mask_1 | bit_next_row,
                    column_mask_2,
                )

            if ((column_mask_1 >> first_empty_row) & 1) == 0 and ((column_mask_1 >> (first_empty_row + 1)) & 1) == 0:
                total_arrangements += count_tilings(
                    column_index,
                    column_mask_0 | bit_current_row,
                    column_mask_1 | bit_current_row | bit_next_row,
                    column_mask_2,
                )

        if first_empty_row - 1 >= 0:
            bit_previous_row = 1 << (first_empty_row - 1)

            if ((column_mask_1 >> first_empty_row) & 1) == 0 and ((column_mask_1 >> (first_empty_row - 1)) & 1) == 0:
                total_arrangements += count_tilings(
                    column_index,
                    column_mask_0 | bit_current_row,
                    column_mask_1 | bit_current_row | bit_previous_row,
                    column_mask_2,
                )

    return total_arrangements


def projecteuler_161() -> int:
    return count_tilings(0, 0, 0, 0)


if __name__ == "__main__":
    print(projecteuler_161())
