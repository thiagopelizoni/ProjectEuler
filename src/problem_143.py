# Problem: https://projecteuler.net/problem=143
import math
import collections
from math import gcd, isqrt

def main():
    maximum_possible_sum = 120000

    pairs_grouped_by_smaller = collections.defaultdict(list)

    maximum_u_value = 400

    for u_value in range(1, maximum_u_value + 1):
        for v_value in range(1, u_value):
            if gcd(u_value, v_value) != 1:
                continue

            if (u_value - v_value) % 3 == 0:
                continue

            a_value = 2 * u_value * v_value + v_value * v_value

            b_value = u_value * u_value - v_value * v_value

            smaller_pair = min(a_value, b_value)

            larger_pair = max(a_value, b_value)

            scale_factor = 1

            while True:
                scaled_smaller = scale_factor * smaller_pair

                scaled_larger = scale_factor * larger_pair

                if scaled_smaller + scaled_larger > maximum_possible_sum:
                    break

                pairs_grouped_by_smaller[scaled_smaller].append(scaled_larger)

                scale_factor += 1

    for smaller_key in pairs_grouped_by_smaller:
        pairs_grouped_by_smaller[smaller_key] = sorted(set(pairs_grouped_by_smaller[smaller_key]))

    unique_sum_values = set()

    for smaller_value in pairs_grouped_by_smaller:
        larger_values_list = pairs_grouped_by_smaller[smaller_value]

        for first_index in range(len(larger_values_list)):
            first_larger_value = larger_values_list[first_index]

            for second_index in range(first_index + 1, len(larger_values_list)):
                second_larger_value = larger_values_list[second_index]

                if first_larger_value in pairs_grouped_by_smaller and second_larger_value in pairs_grouped_by_smaller[first_larger_value]:
                    p_value = smaller_value

                    q_value = first_larger_value

                    r_value = second_larger_value

                    current_total = p_value + q_value + r_value

                    if current_total > maximum_possible_sum:
                        continue

                    a_squared_value = q_value**2 + r_value**2 + q_value * r_value

                    b_squared_value = p_value**2 + r_value**2 + p_value * r_value

                    c_squared_value = p_value**2 + q_value**2 + p_value * q_value

                    side_a_length = isqrt(a_squared_value)

                    side_b_length = isqrt(b_squared_value)

                    side_c_length = isqrt(c_squared_value)

                    if side_a_length**2 != a_squared_value or side_b_length**2 != b_squared_value or side_c_length**2 != c_squared_value:
                        continue

                    if side_a_length + side_b_length <= side_c_length or side_a_length + side_c_length <= side_b_length or side_b_length + side_c_length <= side_a_length:
                        continue

                    if a_squared_value >= b_squared_value + c_squared_value + side_b_length * side_c_length:
                        continue

                    if b_squared_value >= a_squared_value + c_squared_value + side_a_length * side_c_length:
                        continue

                    if c_squared_value >= a_squared_value + b_squared_value + side_a_length * side_b_length:
                        continue

                    unique_sum_values.add(current_total)

    return sum(unique_sum_values)

if __name__ == "__main__":
    print(main())