# Problem: https://projecteuler.net/problem=160
from math import log


def exponent_of_prime_in_factorial(n_value, prime_value):
    total_exponent = 0
    divisor = prime_value
    while divisor <= n_value:
        total_exponent += n_value // divisor
        divisor *= prime_value
    return total_exponent


def modular_inverse(value, modulus):
    return pow(value, -1, modulus)


def build_prefix_products(modulus, prime_value):
    prefix_products = [1] * (modulus + 1)
    running_product = 1
    for current in range(1, modulus + 1):
        if current % prime_value != 0:
            running_product = (running_product * current) % modulus
        prefix_products[current] = running_product
    return prefix_products


def product_of_units_full_block(modulus, prime_value, prefix_products):
    return prefix_products[modulus]


def factorial_without_prime(n_value, prime_value, power_value, prefix_products, block_product):
    if n_value == 0:
        return 1
    modulus = prime_value ** power_value
    full_blocks = n_value // modulus
    remainder = n_value % modulus
    result = pow(block_product, full_blocks, modulus)
    result = (result * prefix_products[remainder]) % modulus
    return (result * factorial_without_prime(n_value // prime_value, prime_value, power_value, prefix_products, block_product)) % modulus


def combine_crt(value_mod_a, value_mod_b, modulus_a, modulus_b):
    modulus_total = modulus_a * modulus_b
    inverse_a = modular_inverse(modulus_a, modulus_b)
    adjustment = (value_mod_b - value_mod_a) % modulus_b
    k_value = (adjustment * inverse_a) % modulus_b
    return (value_mod_a + modulus_a * k_value) % modulus_total


def solve():
    n_value = 10 ** 12

    modulus_two_power = 2 ** 5
    modulus_five_power = 5 ** 5
    modulus_total = modulus_two_power * modulus_five_power

    prefix_two = build_prefix_products(modulus_two_power, 2)
    prefix_five = build_prefix_products(modulus_five_power, 5)

    block_two = product_of_units_full_block(modulus_two_power, 2, prefix_two)
    block_five = product_of_units_full_block(modulus_five_power, 5, prefix_five)

    factorial_wo_twos = factorial_without_prime(n_value, 2, 5, prefix_two, block_two)
    factorial_wo_fives = factorial_without_prime(n_value, 5, 5, prefix_five, block_five)

    exponent_twos = exponent_of_prime_in_factorial(n_value, 2)
    exponent_fives = exponent_of_prime_in_factorial(n_value, 5)

    excess_twos = exponent_twos - exponent_fives

    value_mod_32 = factorial_wo_twos
    inverse_fives_mod_32 = modular_inverse(pow(5, exponent_fives, modulus_two_power), modulus_two_power)
    multiplier_twos_mod_32 = pow(2, excess_twos, modulus_two_power)
    value_mod_32 = (value_mod_32 * inverse_fives_mod_32) % modulus_two_power
    value_mod_32 = (value_mod_32 * multiplier_twos_mod_32) % modulus_two_power

    value_mod_3125 = factorial_wo_fives
    inverse_twos_mod_3125 = modular_inverse(pow(2, exponent_fives, modulus_five_power), modulus_five_power)
    value_mod_3125 = (value_mod_3125 * inverse_twos_mod_3125) % modulus_five_power

    final_value = combine_crt(value_mod_32, value_mod_3125, modulus_two_power, modulus_five_power)
    final_value = final_value % modulus_total

    print(final_value)


if __name__ == "__main__":
    solve()
