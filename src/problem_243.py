# Problem: https://projecteuler.net/problem=243
from fractions import Fraction
from math import ceil
import heapq
from sympy.ntheory import primerange
from tqdm import tqdm
import sys

def find_smallest_smooth_number_greater_or_equal(minimum_m: int, allowed_primes: list[int]) -> int:
    if minimum_m <= 1:
        return 1
    priority_queue = [1]
    visited = {1}
    progress_bar = tqdm(desc="Generating smooth numbers", total=None, file=sys.stdout)
    while priority_queue:
        current_number = heapq.heappop(priority_queue)
        progress_bar.update(1)
        if current_number >= minimum_m:
            progress_bar.close()
            return current_number
        for prime in allowed_primes:
            next_number = current_number * prime
            if next_number not in visited:
                visited.add(next_number)
                heapq.heappush(priority_queue, next_number)
    progress_bar.close()
    return -1

target_ratio = Fraction(15499, 94744)
list_of_primes = list(primerange(2, 1000))
current_primorial = 1
current_totient = 1
list_of_used_primes = []
for current_prime in list_of_primes:
    list_of_used_primes.append(current_prime)
    new_primorial = current_primorial * current_prime
    new_totient = current_totient * (current_prime - 1)
    current_s = Fraction(new_totient, new_primorial)
    if current_s >= target_ratio:
        current_primorial = new_primorial
        current_totient = new_totient
        continue
    numerator_for_threshold = 15499 * new_primorial
    denominator_for_threshold = 15499 * new_primorial - 94744 * new_totient
    floor_value = numerator_for_threshold // denominator_for_threshold
    required_minimum_d = floor_value + 1
    minimum_m_to_reach = (required_minimum_d + new_primorial - 1) // new_primorial
    smallest_m = find_smallest_smooth_number_greater_or_equal(minimum_m_to_reach, list_of_used_primes)
    smallest_denominator = new_primorial * smallest_m
    print(smallest_denominator)
    break