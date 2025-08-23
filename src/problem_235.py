# Problem: https://projecteuler.net/problem=235
from mpmath import mp, mpf, power
from tqdm import tqdm

mp.dps = 20

number_of_terms = 5000
target_value = mpf('-600000000000')

def compute_function(r_value):
    if r_value == 1:
        sum_at_one = 900 * number_of_terms - 3 * number_of_terms * (number_of_terms + 1) / 2
        return sum_at_one - target_value

    power_r_to_n = power(r_value, number_of_terms)
    power_r_to_n_plus_one = power(r_value, number_of_terms + 1)
    one_value = mpf('1')
    term_one = mpf('900') * (one_value - power_r_to_n) / (one_value - r_value)
    term_two = mpf('-3') * (one_value - (number_of_terms + 1) * power_r_to_n + number_of_terms * power_r_to_n_plus_one) / (one_value - r_value) ** 2
    sum_value = term_one + term_two
    return sum_value - target_value

lower_bound = mpf('1.001')
upper_bound = mpf('1.003')

for iteration in tqdm(range(100)):
    midpoint = (lower_bound + upper_bound) / 2
    function_at_midpoint = compute_function(midpoint)

    if function_at_midpoint > 0:
        lower_bound = midpoint
    else:
        upper_bound = midpoint

print(format(float(lower_bound), '.12f'))