# Problem: https://projecteuler.net/problem=162
from typing import List, Sequence


MAX_DIGITS = 16


def digit_mask_map() -> List[int]:
    masks = [0] * 16
    masks[0] = 1
    masks[1] = 2
    masks[10] = 4
    return masks


def apply_step(
    current_state_counts: Sequence[int],
    allowed_digits: Sequence[int],
    digit_masks: Sequence[int],
) -> List[int]:
    next_state_counts = [0] * 8

    for state_index in range(8):
        count_at_state = current_state_counts[state_index]
        if count_at_state == 0:
            continue

        for digit_value in allowed_digits:
            added_mask = digit_masks[digit_value]
            new_state = state_index | added_mask
            next_state_counts[new_state] += count_at_state

    return next_state_counts


def sum_valid_counts_up_to(max_length: int) -> int:
    digit_masks = digit_mask_map()

    first_digit_choices = tuple(range(1, 16))
    other_digit_choices = tuple(range(16))

    state_counts = [0] * 8
    state_counts[0] = 1

    total_valid_numbers = 0

    for current_length in range(1, max_length + 1):
        if current_length == 1:
            state_counts = apply_step(
                state_counts,
                first_digit_choices,
                digit_masks,
            )
        else:
            state_counts = apply_step(
                state_counts,
                other_digit_choices,
                digit_masks,
            )

        total_valid_numbers += state_counts[7]

    return total_valid_numbers


def main() -> str:
    total_count = sum_valid_counts_up_to(MAX_DIGITS)
    return format(total_count, "X")


if __name__ == "__main__":
    print(main())
