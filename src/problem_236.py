# Problem: https://projecteuler.net/problem=236
from fractions import Fraction
import math
from multiprocessing import Pool
from tqdm import tqdm

supplied_by_a = [5248, 1312, 2624, 5760, 3936]
supplied_by_b = [640, 1888, 3776, 3776, 5664]

total_supplied_by_a = sum(supplied_by_a)
total_supplied_by_b = sum(supplied_by_b)


def compute_possible_for_product(product_index):
    number_supplied_by_a = supplied_by_a[product_index]
    number_supplied_by_b = supplied_by_b[product_index]

    possible_m_values = set()

    for spoiled_from_a in tqdm(
        range(1, number_supplied_by_a + 1),
        desc=f"Processing product {product_index + 1}",
    ):
        min_spoiled_from_b = (spoiled_from_a * number_supplied_by_b // number_supplied_by_a) + 1
        min_spoiled_from_b = max(min_spoiled_from_b, 1)

        for spoiled_from_b in range(min_spoiled_from_b, number_supplied_by_b + 1):
            m_fraction = Fraction(
                spoiled_from_b * number_supplied_by_a,
                spoiled_from_a * number_supplied_by_b,
            )
            possible_m_values.add(m_fraction)

    return possible_m_values


def compute_remaining_range(products_list, start_index):
    min_remaining = 0
    max_remaining = 0

    for coefficient, max_k in products_list[start_index:]:
        if coefficient > 0:
            min_remaining += coefficient * 1
            max_remaining += coefficient * max_k
        elif coefficient < 0:
            min_remaining += coefficient * max_k
            max_remaining += coefficient * 1

    return min_remaining, max_remaining


def recursive_check(products_list, index, current_sum):
    if index == len(products_list):
        return current_sum == 0

    coefficient, max_k = products_list[index]

    if coefficient == 0:
        return recursive_check(products_list, index + 1, current_sum)

    min_remaining, max_remaining = compute_remaining_range(products_list, index + 1)

    for k_value in range(1, max_k + 1):
        new_sum = current_sum + coefficient * k_value

        if new_sum + min_remaining > 0 or new_sum + max_remaining < 0:
            continue

        if recursive_check(products_list, index + 1, new_sum):
            return True

    return False


def is_valid_for_this_m(current_m_fraction):
    numerator_m = current_m_fraction.numerator
    denominator_m = current_m_fraction.denominator

    products_list = []

    for product_index in range(5):
        amount_a = supplied_by_a[product_index]
        amount_b = supplied_by_b[product_index]

        gcd_value = math.gcd(denominator_m * amount_a, numerator_m * amount_b)

        d_factor = (denominator_m * amount_a) // gcd_value
        c_factor = (numerator_m * amount_b) // gcd_value

        if d_factor <= 0 or c_factor <= 0:
            return False

        max_k = min(amount_a // d_factor, amount_b // c_factor)

        if max_k < 1:
            return False

        coefficient = (
            denominator_m * total_supplied_by_b * d_factor
            - numerator_m * total_supplied_by_a * c_factor
        )

        products_list.append((coefficient, max_k))

    products_list.sort(key=lambda pair: pair[1])

    return recursive_check(products_list, 0, 0)


with Pool(5) as process_pool:
    all_possible_m_sets = process_pool.map(compute_possible_for_product, range(5))

common_m_values_set = set.intersection(*all_possible_m_sets)

for current_m_fraction in tqdm(
    sorted(common_m_values_set, reverse=True),
    desc="Verifying overall conditions",
):
    if is_valid_for_this_m(current_m_fraction):
        print(f"{current_m_fraction.numerator}/{current_m_fraction.denominator}")
        break