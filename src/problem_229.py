# Problem: https://projecteuler.net/problem=229
import math
from math import isqrt
from tqdm import tqdm
from multiprocessing import Pool

maximum_number = 2_000_000_000
modulus = 168
good_residues = [1, 25, 121]


def generate_small_primes(limit):
    is_prime_flags = [True] * (limit + 1)
    is_prime_flags[0] = False
    is_prime_flags[1] = False

    for number in range(2, isqrt(limit) + 1):
        if is_prime_flags[number]:
            for multiple in range(number * number, limit + 1, number):
                is_prime_flags[multiple] = False

    return [n for n in range(2, limit + 1) if is_prime_flags[n]]


def generate_free_primes_list(limit):
    root_limit = isqrt(limit)
    small_primes = generate_small_primes(root_limit + 1)
    segment_size = 1 << 20
    free_primes = []

    for segment_low in tqdm(range(0, limit + 1, segment_size)):
        segment_high = min(segment_low + segment_size - 1, limit)
        segment_length = segment_high - segment_low + 1
        segment_flags = [True] * segment_length

        if segment_low == 0:
            segment_flags[0] = False
            if segment_high >= 1:
                segment_flags[1] = False

        for prime in small_primes:
            if prime * prime > segment_high:
                break
            start_value = max(segment_low, prime * prime)
            first_multiple = ((start_value + prime - 1) // prime) * prime
            for multiple in range(first_multiple, segment_high + 1, prime):
                segment_flags[multiple - segment_low] = False

        for offset in range(max(segment_low, 2) - segment_low, segment_length):
            if segment_flags[offset]:
                candidate = segment_low + offset
                if candidate % modulus in good_residues:
                    free_primes.append(candidate)

    return free_primes


def compute_total_count(free_primes, limit):
    total = 0
    count_primes = len(free_primes)

    total += isqrt(limit)

    for prime in free_primes:
        if prime > limit:
            break
        total += isqrt(limit // prime)

    for i in range(count_primes):
        first = free_primes[i]
        if first > limit:
            break
        for j in range(i + 1, count_primes):
            product_two = first * free_primes[j]
            if product_two > limit:
                break
            total += isqrt(limit // product_two)

    for i in range(count_primes):
        first = free_primes[i]
        if first > limit:
            break
        for j in range(i + 1, count_primes):
            product_two = first * free_primes[j]
            if product_two > limit:
                break
            for k in range(j + 1, count_primes):
                product_three = product_two * free_primes[k]
                if product_three > limit:
                    break
                total += isqrt(limit // product_three)

    return total


def is_bad_for_given_m(root_value):
    square_value = root_value * root_value
    for coefficient in (1, 2, 3, 7):
        found = False
        max_y = isqrt(square_value // coefficient)
        for y in range(1, max_y + 1):
            remaining = square_value - coefficient * y * y
            x = isqrt(remaining)
            if x * x == remaining and x > 0:
                found = True
                break
        if not found:
            return True
    return False


free_primes = generate_free_primes_list(maximum_number)
total_count = compute_total_count(free_primes, maximum_number)
root_limit = isqrt(maximum_number)

with Pool() as pool:
    results = list(
        tqdm(pool.imap(is_bad_for_given_m, range(1, root_limit + 1)), total=root_limit)
    )

bad_count = sum(1 for r in results if r)
final_result = total_count - bad_count

print(final_result)