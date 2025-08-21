# Problem: https://projecteuler.net/problem=223
import itertools
from tqdm import tqdm
import numpy as np
from sympy import primefactors
from sympy.ntheory import factorint, sieve
from sympy.ntheory.modular import crt

def sieve_smallest_prime_factors(max_value):
    spf = list(range(max_value + 1))
    
    for i in range(2, int(np.sqrt(max_value)) + 1):
        if spf[i] == i:
            for j in range(i*i, max_value + 1, i):
                if spf[j] == j:
                    spf[j] = i
                    
    return spf


def get_factors(number, smallest_prime_factors):   
    if number == 1:
        return {}

    factors = {}

    while number > 1:
        prime_factor = smallest_prime_factors[number]
        count = 0

        while number % prime_factor == 0:
            number //= prime_factor
            count += 1

        factors[prime_factor] = count

    return factors


def compute_solutions_for_power_of_two(exponent):
    if exponent == 1:
        return [1]

    if exponent == 2:
        return [1, 3]

    modulus = 1 << exponent
    half_modulus = modulus >> 1

    return [1, modulus - 1, half_modulus - 1, half_modulus + 1]


def compute_chinese_remainder_theorem(congruences):
    value = 0
    modulus = 1

    for target_congruence, current_modulus in congruences:
        difference = (target_congruence - value) % current_modulus
        inverse = pow(modulus, -1, current_modulus)
        step = difference * inverse % current_modulus

        value += modulus * step
        modulus *= current_modulus
        value %= modulus

    return value


perimeter_limit = 25_000_000
maximum_side_difference = perimeter_limit // 4
smallest_prime_factors = sieve_smallest_prime_factors(maximum_side_difference)
total_barely_acute_triangles = 0

for side_difference in tqdm(range(1, maximum_side_difference + 1)):
    factors = get_factors(side_difference, smallest_prime_factors)
    exponent_two = factors.get(2, 0)
    power_of_two = 1 << (exponent_two + 1)
    odd_part_modulus = side_difference >> exponent_two
    solutions_power_of_two = compute_solutions_for_power_of_two(exponent_two + 1)

    if odd_part_modulus == 1:
        solutions_v = solutions_power_of_two
    else:
        odd_prime_powers = [prime ** factors[prime] for prime in factors if prime != 2]
        number_odd_primes = len(odd_prime_powers)
        sign_products = itertools.product([1, -1], repeat=number_odd_primes)
        solutions_odd_part = []

        for sign_tuple in sign_products:
            congruences = []

            for index, sign in enumerate(sign_tuple):
                mod_power = odd_prime_powers[index]
                target = 1 if sign == 1 else mod_power - 1
                congruences.append((target, mod_power))

            solution_b = compute_chinese_remainder_theorem(congruences)
            solutions_odd_part.append(solution_b)

        solutions_v = []

        for solution_a in solutions_power_of_two:
            for solution_b in solutions_odd_part:
                inverse = pow(power_of_two, -1, odd_part_modulus)
                difference = (solution_b - solution_a) % odd_part_modulus
                step = difference * inverse % odd_part_modulus
                v_value = solution_a + power_of_two * step
                solutions_v.append(v_value)

    modulus = 2 * side_difference
    possible_remainders = [(v + side_difference) % modulus for v in solutions_v]

    for remainder in possible_remainders:
        side_a = remainder

        if side_a < side_difference + 1:
            diff_to_next = side_difference + 1 - side_a
            steps = (diff_to_next + modulus - 1) // modulus
            side_a += steps * modulus

        while True:
            if side_a == 0:
                side_a += modulus
                continue

            squared_a_minus_one = side_a ** 2 - 1
            side_sum_e = squared_a_minus_one // side_difference

            if side_sum_e <= side_difference:
                break

            side_b = (side_sum_e - side_difference) // 2
            perimeter = side_a + side_sum_e

            if perimeter > perimeter_limit:
                break

            if side_b >= side_a:
                total_barely_acute_triangles += 1

            side_a += modulus

if __name__ == "__main__":
    total_barely_acute_triangles += (perimeter_limit - 1) // 2
    print(total_barely_acute_triangles)