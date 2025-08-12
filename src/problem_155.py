# Problem: https://projecteuler.net/problem=155
from fractions import Fraction


def combine_parallel(capacitance_a, capacitance_b):
    return capacitance_a + capacitance_b


def combine_series(capacitance_a, capacitance_b):
    return (capacitance_a * capacitance_b) / (capacitance_a + capacitance_b)


def build_exact_capacitances(max_units):
    exact_sets = {}
    exact_sets[1] = {Fraction(1, 1)}

    for total_units in range(2, max_units + 1):
        new_values = set()

        for left_units in range(1, (total_units // 2) + 1):
            right_units = total_units - left_units

            left_values = list(exact_sets[left_units])
            right_values = list(exact_sets[right_units])

            if left_units == right_units:
                for i in range(len(left_values)):
                    value_a = left_values[i]
                    for j in range(i, len(right_values)):
                        value_b = right_values[j]
                        new_values.add(combine_parallel(value_a, value_b))
                        new_values.add(combine_series(value_a, value_b))
            else:
                for value_a in left_values:
                    for value_b in right_values:
                        new_values.add(combine_parallel(value_a, value_b))
                        new_values.add(combine_series(value_a, value_b))

        exact_sets[total_units] = new_values

    return exact_sets


def count_distinct_up_to(max_units):
    exact_sets = build_exact_capacitances(max_units)
    all_values = set()

    for units in range(1, max_units + 1):
        all_values.update(exact_sets[units])

    return len(all_values)


def solve():
    max_units = 18
    result = count_distinct_up_to(max_units)
    print(result)


if __name__ == "__main__":
    solve()
