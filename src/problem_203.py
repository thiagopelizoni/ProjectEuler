# Problem: https://projecteuler.net/problem=203
import multiprocessing
from math import comb
from sympy import factorint
from tqdm import tqdm

def is_square_free(number):
    if number <= 1:
        return True
    factors = factorint(number)
    return all(exponent < 2 for exponent in factors.values())

number_of_rows = 51
unique_binomial_coefficients = set()

for row in tqdm(range(number_of_rows)):
    for position in range(row + 1):
        binomial_value = comb(row, position)
        unique_binomial_coefficients.add(binomial_value)

sorted_unique_binomials = sorted(unique_binomial_coefficients)

sum_of_squarefree_binomials = 0

with multiprocessing.Pool() as processing_pool:
    squarefree_checks = list(tqdm(
        processing_pool.imap(is_square_free, sorted_unique_binomials),
        total=len(sorted_unique_binomials),
        desc="Checking squarefree"
    ))

for binomial, is_squarefree in zip(sorted_unique_binomials, squarefree_checks):
    if is_squarefree:
        sum_of_squarefree_binomials += binomial

print(sum_of_squarefree_binomials)