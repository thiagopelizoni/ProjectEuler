# Problem: https://projecteuler.net/problem=202
import sympy
from tqdm import tqdm

number_of_bounces = 12017639147
lattice_sum = (number_of_bounces + 3) // 2
prime_factors = sympy.factorint(lattice_sum)
all_divisors = [1]
for prime, exponent in prime_factors.items():
    new_divisors_list = []
    for power in range(1, exponent + 1):
        for existing_divisor in all_divisors:
            new_divisors_list.append(existing_divisor * prime ** power)
    all_divisors.extend(new_divisors_list)
all_divisors.sort()

primitive_points_count = 0
for divisor in tqdm(all_divisors):
    quotient = lattice_sum // divisor
    mobius_value = sympy.mobius(divisor)
    primitive_points_count += mobius_value * quotient

is_square_free = all(exponent == 1 for exponent in prime_factors.values())
if is_square_free:
    correction = 0
else:
    correction = 2 ** len(prime_factors)

number_of_ways = (primitive_points_count - correction) // 3
print(number_of_ways)