# Problem: https://projecteuler.net/problem=204
import multiprocessing
import sympy
from tqdm import tqdm

limit_value = 10**9
list_of_primes = list(sympy.primerange(2, 101))

def recursive_count_function(current_product_value, starting_prime_index):
    if current_product_value > limit_value:
        return 0
    total_count_value = 1
    for prime_index in range(starting_prime_index, len(list_of_primes)):
        current_prime = list_of_primes[prime_index]
        new_product_value = current_product_value * current_prime
        if new_product_value > limit_value:
            break
        total_count_value += recursive_count_function(new_product_value, prime_index)
    return total_count_value

def compute_branch_for_index(prime_index):
    starting_prime = list_of_primes[prime_index]
    initial_product = starting_prime
    if initial_product > limit_value:
        return 0
    return recursive_count_function(initial_product, prime_index)

if __name__ == '__main__':
    with multiprocessing.Pool() as processing_pool:
        branch_results = list(tqdm(
            processing_pool.imap(compute_branch_for_index, range(len(list_of_primes))),
            total=len(list_of_primes),
            desc="Processing branches"
        ))
    final_total = 1 + sum(branch_results)
    print(final_total)