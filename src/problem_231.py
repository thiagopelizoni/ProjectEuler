# Problem: https://projecteuler.net/problem=231
import multiprocessing
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from sympy import sieve

N = 20_000_000
K = 15_000_000

def exponent_in_factorial(number, prime):
    exponent = 0
    power = prime
    while power <= number:
        exponent += number // power
        power *= prime
    return exponent

def compute_contribution(prime):
    exp_n = exponent_in_factorial(N, prime)
    exp_k = exponent_in_factorial(K, prime)
    exp_n_minus_k = exponent_in_factorial(N - K, prime)
    return (exp_n - exp_k - exp_n_minus_k) * prime

if __name__ == "__main__":
    sieve.extend(N)
    primes = list(sieve.primerange(2, N + 1))

    with Pool(cpu_count()) as pool:
        contributions = list(tqdm(pool.imap(compute_contribution, primes), total=len(primes)))

    total_sum = sum(contributions)
    print(total_sum)