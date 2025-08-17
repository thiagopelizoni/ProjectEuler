# Problem: https://projecteuler.net/problem=182
import math
import multiprocessing as mp
from tqdm import tqdm

prime_p = 1009
prime_q = 3643
euler_totient_phi = (prime_p - 1) * (prime_q - 1)
p_minus_one = prime_p - 1
q_minus_one = prime_q - 1

def find_local_minimum_in_range(start_of_range, end_of_range, totient_value, p_minus_1, q_minus_1):
    local_minimum = float('inf')
    for exponent_e in tqdm(range(start_of_range, end_of_range), desc="Finding minimum"):
        if math.gcd(exponent_e, totient_value) == 1:
            gcd_with_p_minus = math.gcd(exponent_e - 1, p_minus_1)
            gcd_with_q_minus = math.gcd(exponent_e - 1, q_minus_1)
            number_unconcealed_messages = (gcd_with_p_minus + 1) * (gcd_with_q_minus + 1)
            if number_unconcealed_messages < local_minimum:
                local_minimum = number_unconcealed_messages
    return local_minimum

def compute_local_sum_of_exponents(start_of_range, end_of_range, totient_value, p_minus_1, q_minus_1, target_minimum):
    local_sum = 0
    for exponent_e in tqdm(range(start_of_range, end_of_range), desc="Summing exponents"):
        if math.gcd(exponent_e, totient_value) == 1:
            gcd_with_p_minus = math.gcd(exponent_e - 1, p_minus_1)
            gcd_with_q_minus = math.gcd(exponent_e - 1, q_minus_1)
            number_unconcealed_messages = (gcd_with_p_minus + 1) * (gcd_with_q_minus + 1)
            if number_unconcealed_messages == target_minimum:
                local_sum += exponent_e
    return local_sum

number_of_cores = mp.cpu_count()
chunk_size_approx = euler_totient_phi // number_of_cores
range_chunks = []
start_current = 2
for core_index in range(number_of_cores):
    end_current = start_current + chunk_size_approx
    if core_index == number_of_cores - 1:
        end_current = euler_totient_phi
    range_chunks.append((start_current, end_current))
    start_current = end_current

with mp.Pool(number_of_cores) as process_pool:
    local_minimums = process_pool.starmap(
        find_local_minimum_in_range,
        [(start, end, euler_totient_phi, p_minus_one, q_minus_one) for start, end in range_chunks]
    )

minimum_unconcealed = min(local_minimums)

with mp.Pool(number_of_cores) as process_pool:
    local_sums = process_pool.starmap(
        compute_local_sum_of_exponents,
        [(start, end, euler_totient_phi, p_minus_one, q_minus_one, minimum_unconcealed) for start, end in range_chunks]
    )

total_sum_of_exponents = sum(local_sums)
print(total_sum_of_exponents)