# Problem: https://projecteuler.net/problem=304
import math
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

MOD = 1234567891011
NUM = 100000
START = 10**14


def sieve_eratos(limit):
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]


def segmented_sieve(low, high, small_primes):
    if low < 2:
        low = 2
    sieve = [True] * (high - low + 1)
    for p in small_primes:
        if p * p > high:
            break
        start = low + (p - low % p) % p
        if start < p * p:
            start = max(start, p * p)
        for j in range(start, high + 1, p):
            sieve[j - low] = False
    primes = [low + i for i in range(len(sieve)) if sieve[i]]
    return primes


def matrix_mult(a, b, mod):
    return [
        [
            (a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod,
            (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod,
        ],
        [
            (a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod,
            (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod,
        ],
    ]


def matrix_pow(base, exp, mod):
    result = [[1, 0], [0, 1]]
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base, mod)
        base = matrix_mult(base, base, mod)
        exp //= 2
    return result


def fib_mod(n, mod):
    if n < 2:
        return n
    power = matrix_pow([[1, 1], [1, 0]], n - 1, mod)
    return power[0][0]


def compute_fib(p):
    return fib_mod(p, MOD)


def main():
    """
    Purpose:
    Solves Project Euler problem 304 by computing the sum of Fibonacci numbers at the first 100,000 primes greater
    than 10^14, modulo 1234567891011.

    Method / Math Rationale:
    Generates small primes up to sqrt(10^14 + delta) using the Sieve of Eratosthenes.
    Uses segmented sieve to find all primes in [10^14 + 1, 10^14 + delta], where delta is an estimate to ensure
    at least 100,000 primes.
    Computes each fib(a(n)) using matrix exponentiation modulo the given modulus for efficiency with large indices.
    Sums the results modulo the modulus, utilizing parallel processing for the Fibonacci computations.

    Complexity:
    - Prime generation: O(sqrt_max log log sqrt_max) for small primes sieve, where sqrt_max ~ 10^7.
    - Segmented sieve: O(delta log log sqrt_max), where delta ~ 3.5e6.
    - Fibonacci computations: O(100000 * log(10^14)) modular operations, parallelized across available CPUs.

    References:
    https://projecteuler.net/problem=304
    """
    ln_start = math.log(START)
    delta = int(NUM * ln_start * 1.1) + 100000
    low = START + 1
    high = START + delta
    small_limit = int(math.sqrt(high)) + 1
    small_primes = sieve_eratos(small_limit)
    all_primes = segmented_sieve(low, high, small_primes)
    if len(all_primes) < NUM:
        raise ValueError("Increase delta for more primes")
    a = all_primes[:NUM]

    with ProcessPoolExecutor() as executor:
        fibs = list(tqdm(executor.map(compute_fib, a), total=NUM, desc="Computing Fibs"))
    sum_b = sum(fibs) % MOD
    print(sum_b)


if __name__ == "__main__":
    main()