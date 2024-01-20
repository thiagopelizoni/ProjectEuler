# Problem: https://projecteuler.net/problem=51
from itertools import combinations
import random

def is_prime(number):
    if number in [2, 3, 5, 7]:
        return True

    divisor = number - 1
    shift_count = 0

    while not divisor % 2:
        shift_count += 1
        divisor = divisor // 2

    for _ in range(4):
        base = random.randint(2, number - 1)
        result = pow(base, divisor, number)

        if result not in [1, number - 1]:
            is_composite = True
            for i in range(shift_count):
                if pow(result, 2 ** i, number) == number - 1:
                    is_composite = False
                    break
            if is_composite:
                return False
    return True

def answer(family_size):
    prime_family = []

    # Start from a 5-digit number to optimize
    number = 56003

    while len(prime_family) < family_size:
        number += 2
        if is_prime(number):
            number_str = str(number)

            for digit in set(number_str):
                family = []

                for replacement in '0123456789':
                    new_number = int(number_str.replace(digit, replacement))
                    if new_number >= 10000 and is_prime(new_number):
                        family.append(new_number)

                if len(family) == family_size:
                    prime_family = sorted(family)
                    return prime_family[0]

print(answer(8))
