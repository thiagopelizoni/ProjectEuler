# Problem: https://projecteuler.net/problem=157
from math import gcd
from sympy import factorint


def divisor_count(value):
    if value == 1:
        return 1
    factors = factorint(value)
    result = 1
    for exponent in factors.values():
        result *= exponent + 1
    return result


def count_solutions_for_n(power_index):
    base_value = 10 ** power_index
    max_exponent = 2 * power_index

    powers_two = [1]
    for _ in range(max_exponent):
        powers_two.append(powers_two[-1] * 2)

    powers_five = [1]
    for _ in range(max_exponent):
        powers_five.append(powers_five[-1] * 5)

    total_with_order = 0
    center_contribution = 0

    for exponent_two in range(max_exponent + 1):
        for exponent_five in range(max_exponent + 1):
            u_value = powers_two[exponent_two] * powers_five[exponent_five]
            v_value = powers_two[max_exponent - exponent_two] * powers_five[max_exponent - exponent_five]

            common_divisor = gcd(base_value + u_value, base_value + v_value)
            contribution = divisor_count(common_divisor)
            total_with_order += contribution

            if exponent_two == power_index and exponent_five == power_index:
                center_contribution = contribution

    total_unordered = (total_with_order + center_contribution) // 2
    return total_unordered


def solve():
    total_sum = 0
    for power_index in range(1, 10):
        total_sum += count_solutions_for_n(power_index)
    print(total_sum)


if __name__ == "__main__":
    solve()
