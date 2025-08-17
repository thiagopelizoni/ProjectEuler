# Problem: https://projecteuler.net/problem=192
import math
import multiprocessing
from tqdm import tqdm
from mpmath import mp, mpf, sqrt as mp_sqrt

mp.dps = 100

def continued_fraction_terms_for_sqrt(given_n):
    a_zero = int(math.sqrt(given_n))
    yield a_zero
    m_value = 0
    d_value = 1
    a_value = a_zero
    while True:
        m_value = d_value * a_value - m_value
        d_value = (given_n - m_value ** 2) // d_value
        a_value = (a_zero + m_value) // d_value
        yield a_value

def best_denominator_for_given_n(given_n):
    denominator_bound = 1000000000000
    sqrt_of_n_for_floor = math.sqrt(given_n)
    a_zero = math.floor(sqrt_of_n_for_floor)
    if a_zero ** 2 == given_n:
        return 0
    cf_terms_generator = continued_fraction_terms_for_sqrt(given_n)
    current_a = next(cf_terms_generator)
    previous_previous_p = 1
    previous_previous_q = 0
    previous_p = current_a
    previous_q = 1
    mp_sqrt_of_n = mp_sqrt(mpf(given_n))
    while True:
        current_a = next(cf_terms_generator)
        current_p = current_a * previous_p + previous_previous_p
        current_q = current_a * previous_q + previous_previous_q
        if current_q > denominator_bound:
            maximum_m_value = (denominator_bound - previous_previous_q) // previous_q
            if maximum_m_value >= 1:
                m_value = min(maximum_m_value, current_a - 1)
                semi_convergent_p = m_value * previous_p + previous_previous_p
                semi_convergent_q = m_value * previous_q + previous_previous_q
                error_for_previous = abs(mpf(previous_p) / mpf(previous_q) - mp_sqrt_of_n)
                error_for_semi = abs(mpf(semi_convergent_p) / mpf(semi_convergent_q) - mp_sqrt_of_n)
                if error_for_semi < error_for_previous:
                    return semi_convergent_q
                else:
                    return previous_q
            else:
                return previous_q
        previous_previous_p = previous_p
        previous_previous_q = previous_q
        previous_p = current_p
        previous_q = current_q

non_square_numbers_list = []
for current_n_value in range(2, 100001):
    floor_sqrt_value = int(math.sqrt(current_n_value))
    if floor_sqrt_value ** 2 != current_n_value:
        non_square_numbers_list.append(current_n_value)

with multiprocessing.Pool() as processing_pool:
    denominators_list = list(tqdm(processing_pool.imap(best_denominator_for_given_n, non_square_numbers_list), total=len(non_square_numbers_list), desc="Processing n values"))

print(sum(denominators_list))