# Problem: https://projecteuler.net/problem=221
import math
import multiprocessing
from sympy import factorint
from tqdm import tqdm


def get_divisors(number):
    factors = factorint(number)
    divisors = [1]
    for prime, exponent in factors.items():
        powers = [prime ** power for power in range(exponent + 1)]
        new_divisors = []
        for existing in divisors:
            for p in powers:
                new_divisors.append(existing * p)
        divisors = new_divisors
    return sorted(divisors)


def compute_alexandrian_for_p(p_value):
    n_value = p_value * p_value + 1
    divisors = get_divisors(n_value)
    sqrt_n = math.sqrt(n_value)
    alexandrian_list = []
    for divisor in divisors:
        if divisor > sqrt_n:
            break
        corresponding_e = n_value // divisor
        alexandrian = p_value * (p_value + divisor) * (p_value + corresponding_e)
        alexandrian_list.append(alexandrian)
    return alexandrian_list


maximum_p_value = 100_000
all_alexandrian_integers = []

with multiprocessing.Pool() as pool:
    for chunk in tqdm(pool.imap_unordered(compute_alexandrian_for_p, range(1, maximum_p_value + 1)),
                      total=maximum_p_value, desc="Processing p values"):
        all_alexandrian_integers.extend(chunk)

all_alexandrian_integers.sort()

unique_alexandrian_integers = []
previous_value = None
for value in all_alexandrian_integers:
    if value != previous_value:
        unique_alexandrian_integers.append(value)
        previous_value = value

print(unique_alexandrian_integers[149999])