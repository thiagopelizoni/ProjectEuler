# Problem: https://projecteuler.net/problem=248
from math import factorial
from sympy import factorint
from sympy.ntheory import isprime
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm


def get_all_divisors(number_factors):
    prime_factors = list(number_factors.keys())
    exponent_ranges = [range(number_factors[prime] + 1) for prime in prime_factors]
    all_divisors = []

    for exponents in product(*exponent_ranges):
        divisor = 1
        for prime, exponent in zip(prime_factors, exponents):
            divisor *= prime ** exponent
        all_divisors.append(divisor)

    return sorted(all_divisors)


def search(
    remaining_phi_value,
    current_number,
    min_prime_index,
    found_numbers,
    candidate_primes,
):
    if remaining_phi_value == 1:
        found_numbers.append(current_number)
        return

    for prime_index in range(min_prime_index, len(candidate_primes)):
        prime = candidate_primes[prime_index]

        if remaining_phi_value % (prime - 1) == 0:
            new_remaining_phi_value = remaining_phi_value // (prime - 1)
            new_number = current_number * prime
            search(
                new_remaining_phi_value,
                new_number,
                prime_index + 1,
                found_numbers,
                candidate_primes,
            )

            phi_part_with_prime_powers = new_remaining_phi_value
            number_with_prime_powers = new_number

            while phi_part_with_prime_powers % prime == 0:
                phi_part_with_prime_powers //= prime
                number_with_prime_powers *= prime
                search(
                    phi_part_with_prime_powers,
                    number_with_prime_powers,
                    prime_index + 1,
                    found_numbers,
                    candidate_primes,
                )


def process_start(start_prime_index, target_phi_value, candidate_primes):
    found_numbers = []
    prime = candidate_primes[start_prime_index]

    if target_phi_value % (prime - 1) == 0:
        new_remaining_phi_value = target_phi_value // (prime - 1)
        new_number = prime
        search(
            new_remaining_phi_value,
            new_number,
            start_prime_index + 1,
            found_numbers,
            candidate_primes,
        )

        phi_part_with_prime_powers = new_remaining_phi_value
        number_with_prime_powers = new_number

        while phi_part_with_prime_powers % prime == 0:
            phi_part_with_prime_powers //= prime
            number_with_prime_powers *= prime
            search(
                phi_part_with_prime_powers,
                number_with_prime_powers,
                start_prime_index + 1,
                found_numbers,
                candidate_primes,
            )

    return found_numbers


def main():
    target_phi_value = factorial(13)
    factors_of_target = factorint(target_phi_value)
    divisors_of_target = get_all_divisors(factors_of_target)
    candidate_primes = [
        divisor + 1 for divisor in divisors_of_target if isprime(divisor + 1)
    ]
    candidate_primes.sort()

    with ProcessPoolExecutor() as executor:
        tasks = [
            executor.submit(
                process_start, i, target_phi_value, candidate_primes
            )
            for i in range(len(candidate_primes))
        ]
        all_found_numbers = []
        progress_bar = tqdm(
            as_completed(tasks),
            total=len(tasks),
            desc="Processing starting primes",
        )
        for future in progress_bar:
            all_found_numbers.extend(future.result())

    all_found_numbers.sort()
    print(all_found_numbers[149999])


if __name__ == "__main__":
    main()