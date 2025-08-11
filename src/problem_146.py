# Problem: https://projecteuler.net/problem=146
from math import gcd
from gmpy2 import is_prime


def build_allowed_residues(modulus_value, prime_list, prime_offsets):
    allowed_residues = []

    for residue_value in range(modulus_value):
        residue_squared = (residue_value * residue_value) % modulus_value
        valid_residue = True

        for prime_value in prime_list:
            residue_mod_prime = residue_squared % prime_value

            for offset_value in prime_offsets:
                if (residue_mod_prime + offset_value) % prime_value == 0:
                    valid_residue = False
                    break

            if not valid_residue:
                break

        if valid_residue:
            allowed_residues.append(residue_value)

    return allowed_residues


def combine_with_mod_ten(residue_value, modulus_value, step_value):
    current_value = residue_value % step_value

    while current_value % 10 != 0:
        current_value += modulus_value

    return current_value


def passes_prime_pattern(n_value, prime_offsets, composite_offsets):
    n_squared = n_value * n_value

    for offset_value in prime_offsets:
        if not is_prime(n_squared + offset_value):
            return False

    for offset_value in composite_offsets:
        if is_prime(n_squared + offset_value):
            return False

    return True


def sum_special_numbers(limit_value):
    prime_offsets = [1, 3, 7, 9, 13, 27]
    composite_offsets = [5, 11, 15, 17, 19, 21, 23, 25]

    wheel_primes = [3, 7, 11, 13, 17, 19]
    wheel_modulus = 1

    for prime_value in wheel_primes:
        wheel_modulus *= prime_value

    step_value = wheel_modulus * 10 // gcd(wheel_modulus, 10)

    allowed_residues = build_allowed_residues(wheel_modulus, wheel_primes, prime_offsets)

    total_sum = 0

    for residue_value in allowed_residues:
        start_value = combine_with_mod_ten(residue_value, wheel_modulus, step_value)

        n_value = start_value

        while n_value < limit_value:
            if passes_prime_pattern(n_value, prime_offsets, composite_offsets):
                total_sum += n_value
            n_value += step_value

    return total_sum


def main():
    limit_value = 150_000_000
    result_value = sum_special_numbers(limit_value)
    print(result_value)


if __name__ == "__main__":
    main()
