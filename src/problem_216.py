# Problem: https://projecteuler.net/problem=216
import math
import numpy as np
from tqdm import tqdm

def is_prime(number):
    if number <= 1:
        return False
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    divisor = 5
    while divisor * divisor <= number:
        if number % divisor == 0 or number % (divisor + 2) == 0:
            return False
        divisor += 6
    return True

def modular_sqrt(residue, prime):
    if residue == 0:
        return 0
    if prime == 2:
        return residue
    legendre_symbol = pow(residue, (prime - 1) // 2, prime)
    if legendre_symbol != 1:
        return None
    if prime % 4 == 3:
        return pow(residue, (prime + 1) // 4, prime)
    exponent_s = prime - 1
    exponent_e = 0
    while exponent_s % 2 == 0:
        exponent_s //= 2
        exponent_e += 1
    non_residue = 2
    while pow(non_residue, (prime - 1) // 2, prime) != prime - 1:
        non_residue += 1
    current_m = exponent_e
    current_c = pow(non_residue, exponent_s, prime)
    current_t = pow(residue, exponent_s, prime)
    current_r = pow(residue, (exponent_s + 1) // 2, prime)
    while True:
        if current_t == 0:
            return 0
        if current_t == 1:
            return current_r
        current_i = 1
        temp_t = pow(current_t, 2, prime)
        while temp_t != 1:
            temp_t = pow(temp_t, 2, prime)
            current_i += 1
        if current_i == current_m:
            return None
        power_for_b = 1 << (current_m - current_i - 1)
        current_b = pow(current_c, power_for_b, prime)
        current_r = (current_r * current_b) % prime
        current_c = (current_b * current_b) % prime
        current_t = (current_t * current_c) % prime
        current_m = current_i

def generate_primes_up_to(limit):
    if limit < 2:
        return np.array([], dtype=int)
    is_prime_array = np.ones(limit + 1, dtype=bool)
    is_prime_array[0:2] = False
    for num in range(2, int(math.sqrt(limit)) + 1):
        if is_prime_array[num]:
            is_prime_array[num * num::num] = False
    return np.nonzero(is_prime_array)[0]

if __name__ == "__main__":
    max_number = 50000000
    sieve_limit = int(math.sqrt(2 * max_number * max_number - 1)) + 10
    all_small_primes = generate_primes_up_to(sieve_limit)
    small_primes = [int(prime) for prime in all_small_primes[all_small_primes > 2]]
    candidates = np.ones(max_number + 1, dtype=bool)
    candidates[0] = candidates[1] = False
    for prime in tqdm(small_primes):
        inverse_of_two = pow(2, prime - 2, prime)
        target_value = inverse_of_two % prime
        euler_criterion = pow(target_value, (prime - 1) // 2, prime)
        if euler_criterion == prime - 1:
            euler_criterion = -1
        if euler_criterion != 1:
            continue
        sqrt_one = modular_sqrt(target_value, prime)
        if sqrt_one is None:
            continue
        sqrt_two = (prime - sqrt_one) % prime
        roots = [sqrt_one, sqrt_two] if sqrt_one != sqrt_two else [sqrt_one]
        for root in roots:
            candidates[root::prime] = False
    small_n_limit = int(math.sqrt((sieve_limit + 1) / 2)) + 1
    small_prime_count = 0
    for n in range(2, small_n_limit + 1):
        t_value = 2 * n * n - 1
        if is_prime(t_value):
            small_prime_count += 1
    total_count = small_prime_count + np.sum(candidates)
    print(total_count)