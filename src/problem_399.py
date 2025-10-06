# Problem: https://projecteuler.net/problem=399
import math
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal, getcontext, ROUND_FLOOR
from tqdm import tqdm
import numpy as np

def generate_primes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(2, limit + 1) if is_prime[i]]

def matrix_mul(a, b, mod):
    return [
        [(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod, (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod],
        [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod, (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod]
    ]

def matrix_pow(mat, exp, mod):
    res = [[1, 0], [0, 1]]
    while exp > 0:
        if exp % 2 == 1:
            res = matrix_mul(res, mat, mod)
        mat = matrix_mul(mat, mat, mod)
        exp //= 2
    return res

def fib_mod(n, mod):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    mat = [[1, 1], [1, 0]]
    res = matrix_pow(mat, n - 1, mod)
    return res[0][0]

def get_divisors(n):
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors.sort()
    return divisors

def compute_z(p):
    if p <= 5:
        return None
    mod5 = p % 5
    if mod5 in [1, 4]:
        potential = p - 1
    elif mod5 in [2, 3]:
        potential = 2 * (p + 1)
    else:
        return None
    divs = get_divisors(potential)
    for d in divs:
        if fib_mod(d, p) == 0:
            return d
    return None

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 399 by finding the 100,000,000th squarefree Fibonacci number and
    outputting its last 16 digits followed by its scientific notation rounded to one digit after the
    decimal point.

    Method / Math Rationale
    -----------------------
    Utilizes Wall's conjecture assuming the first Fibonacci number divisible by prime p^2 occurs at
    index p * Z(p), where Z(p) is the rank of appearance of p in the Fibonacci sequence. Computes
    Z(p) by checking Fibonacci values modulo p for divisors of the appropriate potential period
    (p-1 or 2(p+1) based on p mod 5). Collects indices I_p = p * Z(p) <= estimated max_N. Marks
    non-squarefree indices in a boolean array via sieving. Iterates to find the target index n.
    Computes F_n mod 10^16 using matrix exponentiation and approximates scientific notation using
    Binet's formula with high-precision decimals.

    Complexity
    ----------
    O(PI * D * log P) for Z(p) computations where PI ~ 10^6 primes, D ~ 10 average divisors,
    log P ~ 20; O(N) for index finding with N ~ 1.65*10^8.

    References
    ----------
    https://projecteuler.net/problem=399
    """
    target = 100000000
    prime_limit = 20000000
    max_n = 200000000
    mod_last = 10**16

    primes = generate_primes(prime_limit)

    square_indexes = [6, 12, 25]

    primes_to_compute = [p for p in primes if p > 5]

    with ProcessPoolExecutor() as executor:
        zs = list(tqdm(executor.map(compute_z, primes_to_compute), total=len(primes_to_compute)))

    for i, p in enumerate(primes_to_compute):
        z = zs[i]
        if z is not None:
            I = p * z
            if I <= max_n:
                square_indexes.append(I)

    square_indexes = list(set(square_indexes))

    is_non_sqfree = np.zeros(max_n + 1, dtype=bool)
    for I in square_indexes:
        is_non_sqfree[I::I] = True

    count = 0
    n = 0
    for m in range(1, max_n + 1):
        if not is_non_sqfree[m]:
            count += 1
            if count == target:
                n = m
                break

    last16 = str(fib_mod(n, mod_last)).zfill(16)[-16:]

    getcontext().prec = 50
    phi = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    log10_fn = Decimal(n) * phi.log10() - Decimal(5).sqrt().log10()
    floor_log = log10_fn.quantize(Decimal('1'), rounding=ROUND_FLOOR)
    frac_part = log10_fn - floor_log
    mantissa = Decimal(10) ** frac_part
    rounded_mant = round(mantissa, 1)
    exponent = floor_log
    if rounded_mant >= Decimal('10'):
        rounded_mant /= Decimal('10')
        exponent += 1
    sci_not = f"{rounded_mant:.1f}e{exponent}"

    print(f"{last16},{sci_not}")

if __name__ == "__main__":
    main()