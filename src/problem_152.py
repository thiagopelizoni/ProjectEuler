# Problem: https://projecteuler.net/problem=152
from fractions import Fraction

def get_candidates():
    return (
        2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 18, 20, 21, 24,
        28, 30, 35, 36, 39, 40, 42, 45, 52, 56, 60, 63, 70, 72
    )


def build_remaining_sums(candidates):
    remaining_sums = {}
    running_total = Fraction(0, 1)

    for number_value in reversed(candidates):
        running_total += Fraction(1, number_value * number_value)
        remaining_sums[number_value] = running_total

    return remaining_sums


def build_last_subset_sums(candidates, threshold_value):
    tail_numbers = [n for n in candidates if n >= threshold_value]
    total_masks = 1 << len(tail_numbers)

    sums_counter = {}

    for mask in range(total_masks):
        current_sum = Fraction(0, 1)
        index = 0
        temp = mask

        while temp:
            if temp & 1:
                number_value = tail_numbers[index]
                current_sum += Fraction(1, number_value * number_value)
            index += 1
            temp >>= 1

        sums_counter[current_sum] = sums_counter.get(current_sum, 0) + 1

    return sums_counter


def search_sum(
    target_sum,
    candidates,
    remaining,
    last_counter,
    threshold_value,
    start_index,
    current_sum,
):
    if current_sum == target_sum:
        return 1

    if target_sum < current_sum:
        return 0

    if start_index == len(candidates):
        return 0

    number_value = candidates[start_index]
    max_possible_sum = current_sum + remaining[number_value]

    if max_possible_sum < target_sum:
        return 0

    if number_value >= threshold_value:
        difference = target_sum - current_sum
        return last_counter.get(difference, 0)

    total_count = 0

    total_count += search_sum(
        target_sum,
        candidates,
        remaining,
        last_counter,
        threshold_value,
        start_index + 1,
        current_sum,
    )

    total_count += search_sum(
        target_sum,
        candidates,
        remaining,
        last_counter,
        threshold_value,
        start_index + 1,
        current_sum + Fraction(1, number_value * number_value),
    )

    return total_count


def compute_number_of_ways():
    target_sum = Fraction(1, 2)

    candidates = list(get_candidates())
    candidates.sort()

    remaining = build_remaining_sums(candidates)

    threshold_value = 40
    last_counter = build_last_subset_sums(candidates, threshold_value)

    return search_sum(
        target_sum,
        candidates,
        remaining,
        last_counter,
        threshold_value,
        0,
        Fraction(0, 1),
    )


def main():
    result_value = compute_number_of_ways()
    print(result_value)


if __name__ == "__main__":
    main()