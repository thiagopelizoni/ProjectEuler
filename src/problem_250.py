# Problem: https://projecteuler.net/problem=250
from os import cpu_count
from concurrent.futures import ProcessPoolExecutor
from itertools import islice
from tqdm import tqdm


MOD_SUM = 250
LIMIT = 250250
MOD_VALUE = 10 ** 16


def circular_convolution(polynomial_a, polynomial_b, mod_value):
    size = len(polynomial_a)
    result_polynomial = [0] * size

    for index_a in range(size):
        value_a = polynomial_a[index_a]
        if value_a == 0:
            continue

        for index_b in range(size):
            value_b = polynomial_b[index_b]
            if value_b == 0:
                continue

            result_index = (index_a + index_b) % size
            term = value_a * value_b
            result_polynomial[result_index] = (result_polynomial[result_index] + term) % mod_value

    return result_polynomial


def polynomial_power_monomial(residue, exponent, mod_value):
    size = MOD_SUM
    result_polynomial = [0] * size
    result_polynomial[0] = 1

    base_polynomial = [0] * size
    base_polynomial[0] = 1
    base_polynomial[residue % size] = 1

    current_exponent = exponent
    while current_exponent > 0:
        if current_exponent % 2 == 1:
            result_polynomial = circular_convolution(result_polynomial, base_polynomial, mod_value)
        
        base_polynomial = circular_convolution(base_polynomial, base_polynomial, mod_value)
        current_exponent //= 2

    return result_polynomial


def count_residue_chunk(bounds):
    start, end = bounds
    counts = [0] * MOD_SUM

    for number in range(start, end + 1):
        residue = pow(number, number, MOD_SUM)
        counts[residue] += 1
        
    return counts


def compute_poly_for_residue(task):
    residue, frequency, mod_value = task

    if frequency == 0:
        return residue, None

    if residue % MOD_SUM == 0:
        polynomial = [0] * MOD_SUM
        polynomial[0] = pow(2, frequency, mod_value)
        return residue, polynomial

    polynomial = polynomial_power_monomial(residue, frequency, mod_value)
    return residue, polynomial


def chunk_ranges(start, stop, step):
    current = start
    while current <= stop:
        end = min(current + step - 1, stop)
        yield current, end
        current = end + 1


def solve():
    workers = max(1, cpu_count() or 1)
    chunk_size = 2500
    ranges = list(chunk_ranges(1, LIMIT, chunk_size))

    residue_counts = [0] * MOD_SUM
    with ProcessPoolExecutor(max_workers=workers) as executor:
        iterator = executor.map(count_residue_chunk, ranges)
        for counts in tqdm(iterator, total=len(ranges), desc="Counting residues"):
            for i in range(MOD_SUM):
                residue_counts[i] += counts[i]

    tasks = [(r, residue_counts[r], MOD_VALUE) for r in range(MOD_SUM) if residue_counts[r] > 0]

    polynomials = []
    scalar_factor = 1
    with ProcessPoolExecutor(max_workers=workers) as executor:
        iterator = executor.map(compute_poly_for_residue, tasks)
        for residue, polynomial in tqdm(iterator, total=len(tasks), desc="Computing polynomials"):
            if polynomial is None:
                continue
            
            if residue == 0:
                scalar_factor = (scalar_factor * polynomial[0]) % MOD_VALUE
            else:
                polynomials.append(polynomial)

    final_polynomial = [0] * MOD_SUM
    final_polynomial[0] = 1

    for polynomial in tqdm(polynomials, total=len(polynomials), desc="Performing convolutions"):
        final_polynomial = circular_convolution(final_polynomial, polynomial, MOD_VALUE)

    if scalar_factor != 1:
        final_polynomial = [(x * scalar_factor) % MOD_VALUE for x in final_polynomial]

    answer = (final_polynomial[0] - 1) % MOD_VALUE
    print(str(answer).zfill(16))


if __name__ == "__main__":
    solve()
