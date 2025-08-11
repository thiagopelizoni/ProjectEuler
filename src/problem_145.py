# Problem: https://projecteuler.net/problem=145
def build_counts_outer():
    counts = {}
    for sum_value in range(2, 19):
        lower = max(1, sum_value - 9)
        upper = min(9, sum_value - 1)
        counts[sum_value] = max(0, upper - lower + 1)
    return counts


def build_counts_inner():
    counts = {}
    for sum_value in range(0, 19):
        lower = max(0, sum_value - 9)
        upper = min(9, sum_value)
        counts[sum_value] = max(0, upper - lower + 1)
    return counts


def build_counts_middle():
    counts = {k: 0 for k in range(0, 19)}
    for digit_value in range(10):
        counts[2 * digit_value] += 1
    return counts


def check_sum_sequence(sum_sequence):
    carry_value = 0
    total_digits = len(sum_sequence)

    for sum_value in sum_sequence:
        if (sum_value + carry_value) % 2 == 0:
            return False
        carry_value = 1 if sum_value + carry_value >= 10 else 0

    return carry_value == (total_digits % 2)


def count_reversible_by_length(total_digits):
    if total_digits == 1:
        return 0

    outer_counts = build_counts_outer()
    inner_counts = build_counts_inner()
    middle_counts = build_counts_middle()

    half_length = total_digits // 2
    total_count = 0

    stack = [(0, 0, 1, [])]

    while stack:
        position_index, carry_value, ways_count, chosen_sums = stack.pop()

        if position_index == half_length:
            if total_digits % 2 == 1:
                for middle_sum, middle_ways in middle_counts.items():
                    if middle_ways == 0:
                        continue
                    if (middle_sum + carry_value) % 2 == 0:
                        continue
                    full_sequence = chosen_sums + [middle_sum] + chosen_sums[::-1]
                    if check_sum_sequence(full_sequence):
                        total_count += ways_count
            else:
                full_sequence = chosen_sums + chosen_sums[::-1]
                if check_sum_sequence(full_sequence):
                    total_count += ways_count
            continue

        counts_map = outer_counts if position_index == 0 else inner_counts

        for sum_value, pair_ways in counts_map.items():
            if pair_ways == 0:
                continue
            if (sum_value + carry_value) % 2 == 0:
                continue
            next_carry = 1 if sum_value + carry_value >= 10 else 0
            stack.append(
                (
                    position_index + 1,
                    next_carry,
                    ways_count * pair_ways,
                    chosen_sums + [sum_value],
                )
            )

    return total_count


def compute_total_reversible(limit_value):
    max_digits = len(str(limit_value - 1))
    total_count = 0

    for digit_count in range(1, max_digits + 1):
        if 10 ** (digit_count - 1) >= limit_value:
            break
        total_count += count_reversible_by_length(digit_count)

    return total_count


def main():
    limit_value = 10**9
    result_value = compute_total_reversible(limit_value)
    print(result_value)


if __name__ == "__main__":
    main()
