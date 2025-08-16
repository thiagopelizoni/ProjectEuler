# Problem: https://projecteuler.net/problem=176
import math
import gmpy2
from tqdm import tqdm

odd_primes_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

memory_cache = {}
INF = gmpy2.mpz(10) ** 10000
MPZ_TWO = gmpy2.mpz(2)


def ensure_prime_available(index):
    last_candidate = odd_primes_list[-1]
    while index >= len(odd_primes_list):
        last_candidate += 2
        while not gmpy2.is_prime(last_candidate):
            last_candidate += 2
        odd_primes_list.append(int(last_candidate))


def odd_divisors_up_to(number, limit_value):
    upper_limit = math.isqrt(number)
    divisors = set()
    for small_divisor in range(1, upper_limit + 1):
        if number % small_divisor == 0:
            large_divisor = number // small_divisor
            if small_divisor % 2 == 1 and 3 <= small_divisor <= limit_value:
                divisors.add(small_divisor)
            if large_divisor % 2 == 1 and 3 <= large_divisor <= limit_value:
                divisors.add(large_divisor)
    return sorted(divisors)


def recursive_helper_function(
    current_remaining_value,
    maximum_allowed_h_value,
    current_prime_position,
):
    if current_remaining_value == 1:
        return gmpy2.mpz(1)

    cache_key = (
        current_remaining_value,
        maximum_allowed_h_value,
        current_prime_position,
    )
    if cache_key in memory_cache:
        return memory_cache[cache_key]

    smallest_possible_value = INF
    candidate_values = odd_divisors_up_to(
        current_remaining_value,
        maximum_allowed_h_value,
    )

    for candidate_h_value in candidate_values:
        ensure_prime_available(current_prime_position)
        current_exponent = (candidate_h_value - 1) // 2
        selected_prime = gmpy2.mpz(odd_primes_list[current_prime_position])
        next_remaining_value = current_remaining_value // candidate_h_value

        recursive_sub_result = recursive_helper_function(
            next_remaining_value,
            candidate_h_value,
            current_prime_position + 1,
        )

        if recursive_sub_result < INF:
            calculated_value = (
                selected_prime ** current_exponent * recursive_sub_result
            )
            if calculated_value < smallest_possible_value:
                smallest_possible_value = calculated_value

    memory_cache[cache_key] = smallest_possible_value
    return smallest_possible_value


def generate_all_divisors_from_number(input_number):
    divisors_set = set()
    limit_value = math.isqrt(input_number)
    for potential_divisor in range(1, limit_value + 1):
        if input_number % potential_divisor == 0:
            divisors_set.add(potential_divisor)
            divisors_set.add(input_number // potential_divisor)
    return sorted(divisors_set)


target_divisor_count_for_square = 95095
list_of_all_possible_d_values = generate_all_divisors_from_number(
    target_divisor_count_for_square
)
absolute_smallest_m_value = INF

for current_d_value in tqdm(list_of_all_possible_d_values):
    memory_cache.clear()
    current_s_value = target_divisor_count_for_square // current_d_value
    calculated_a_value = (current_d_value + 1) // 2
    computed_k_value = recursive_helper_function(
        current_s_value,
        current_s_value,
        0,
    )
    if computed_k_value < INF:
        computed_m_value = MPZ_TWO ** calculated_a_value * computed_k_value
        if computed_m_value < absolute_smallest_m_value:
            absolute_smallest_m_value = computed_m_value

memory_cache.clear()
computed_odd_k_value = recursive_helper_function(
    target_divisor_count_for_square,
    target_divisor_count_for_square,
    0,
)
if computed_odd_k_value < INF and computed_odd_k_value < absolute_smallest_m_value:
    absolute_smallest_m_value = computed_odd_k_value

print(absolute_smallest_m_value)
