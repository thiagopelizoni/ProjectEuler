# Problem: https://projecteuler.net/problem=151
from functools import lru_cache


def is_single_sheet(state_tuple):
    return sum(state_tuple) == 1 and state_tuple != (0, 0, 0, 1)


def next_state_from_choice(state_tuple, choice_index):
    a2, a3, a4, a5 = state_tuple

    if choice_index == 0:
        return a2 - 1, a3 + 1, a4 + 1, a5 + 1

    if choice_index == 1:
        return a2, a3 - 1, a4 + 1, a5 + 1

    if choice_index == 2:
        return a2, a3, a4 - 1, a5 + 1

    return a2, a3, a4, a5 - 1


@lru_cache(maxsize=None)
def expected_singleton_count(state_tuple):
    if sum(state_tuple) == 0:
        return 0.0

    add_one = 1.0 if is_single_sheet(state_tuple) else 0.0

    total_sheets = sum(state_tuple)
    expectation_sum = 0.0

    for idx, count_value in enumerate(state_tuple):
        if count_value == 0:
            continue
        next_state = next_state_from_choice(state_tuple, idx)
        expectation_sum += (count_value / total_sheets) * expected_singleton_count(next_state)

    return add_one + expectation_sum


def main():
    initial_state = (1, 1, 1, 1)
    result_value = expected_singleton_count(initial_state)
    print(f"{result_value:.6f}")


if __name__ == "__main__":
    main()
