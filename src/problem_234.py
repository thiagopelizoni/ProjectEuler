# Problem: https://projecteuler.net/problem=234
import math
from tqdm import tqdm
from sympy.ntheory import sieve

limit = 999966663333
max_prime_limit = 10**6 + 10**5
primes_list = list(sieve.primerange(2, max_prime_limit))

def sum_of_multiples_in_range(divisor, lower_bound, upper_bound):
    if lower_bound > upper_bound:
        return 0
    first_multiple = ((lower_bound + divisor - 1) // divisor) * divisor
    if first_multiple > upper_bound:
        return 0
    last_multiple = (upper_bound // divisor) * divisor
    number_of_terms = ((last_multiple - first_multiple) // divisor) + 1
    return number_of_terms * (first_multiple + last_multiple) // 2

total_sum_of_semidivisible_numbers = 0

for index in tqdm(range(len(primes_list) - 1)):
    lower_prime = primes_list[index]
    upper_prime = primes_list[index + 1]
    lower_bound = lower_prime * lower_prime + 1
    if lower_bound > limit:
        break
    upper_bound = min(limit, upper_prime * upper_prime - 1)
    if lower_bound > upper_bound:
        continue
    sum_multiples_lower = sum_of_multiples_in_range(lower_prime, lower_bound, upper_bound)
    sum_multiples_upper = sum_of_multiples_in_range(upper_prime, lower_bound, upper_bound)
    sum_multiples_both = sum_of_multiples_in_range(lower_prime * upper_prime, lower_bound, upper_bound)
    contribution = sum_multiples_lower + sum_multiples_upper - 2 * sum_multiples_both
    total_sum_of_semidivisible_numbers += contribution

print(total_sum_of_semidivisible_numbers)