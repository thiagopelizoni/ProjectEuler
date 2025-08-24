# Problem: https://projecteuler.net/problem=239
import math

from decimal import Decimal, getcontext
from fractions import Fraction
from tqdm import tqdm

getcontext().prec = 30

number_of_primes = 25
number_of_fixed_primes = 3
number_of_deranged_primes = number_of_primes - number_of_fixed_primes
total_disks = 100
remaining_disks = total_disks - number_of_fixed_primes

ways_to_choose_fixed_primes = math.comb(number_of_primes, number_of_fixed_primes)

partial_derangement_ways = 0
for j in tqdm(range(number_of_deranged_primes + 1)):
    sign = (-1) ** j
    choose = math.comb(number_of_deranged_primes, j)
    factorial_term = math.factorial(remaining_disks - j)
    term = sign * choose * factorial_term
    partial_derangement_ways += term

favorable_outcomes = ways_to_choose_fixed_primes * partial_derangement_ways
total_outcomes = math.factorial(total_disks)
probability_fraction = Fraction(favorable_outcomes, total_outcomes)
probability_decimal = Decimal(probability_fraction.numerator) / Decimal(probability_fraction.denominator)

print(f"{probability_decimal:.12f}")