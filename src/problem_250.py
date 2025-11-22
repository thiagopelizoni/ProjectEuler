# Problem: https://projecteuler.net/problem=250
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from typing import List, Tuple

def modular_polynomial_multiply(
    poly_a: List[int], poly_b: List[int], modulus: int
) -> List[int]:
    size = len(poly_a)
    result = [0] * size
    for i in range(size):
        coeff_a = poly_a[i]
        if coeff_a == 0:
            continue
        for j in range(size):
            coeff_b = poly_b[j]
            if coeff_b == 0:
                continue
            k = (i + j) % size
            term = coeff_a * coeff_b
            result[k] = (result[k] + term) % modulus
    return result

def compute_monomial_power(
    residue: int, exponent: int, size: int, modulus: int
) -> List[int]:
    result = [0] * size
    result[0] = 1
    base = [0] * size
    base[0] = 1
    base[residue] += 1
    current_exponent = exponent
    while current_exponent > 0:
        if current_exponent % 2 == 1:
            result = modular_polynomial_multiply(result, base, modulus)
        base = modular_polynomial_multiply(base, base, modulus)
        current_exponent //= 2
    return result

def count_residues_in_range(bounds: Tuple[int, int], residue_mod: int) -> List[int]:
    start, end = bounds
    counts = [0] * residue_mod
    for num in range(start, end + 1):
        residue = pow(num, num, residue_mod)
        counts[residue] += 1
    return counts

def compute_residue_polynomial(
    task: Tuple[int, int, int]
) -> Tuple[int, List[int] | None]:
    residue, frequency, modulus = task
    if frequency == 0:
        return residue, None
    size = 250
    if residue == 0:
        poly = [0] * size
        poly[0] = pow(2, frequency, modulus)
        return residue, poly
    poly = compute_monomial_power(residue, frequency, size, modulus)
    return residue, poly

def generate_chunk_ranges(start: int, stop: int, chunk_size: int):
    current = start
    while current <= stop:
        end = min(current + chunk_size - 1, stop)
        yield current, end
        current = end + 1

def main() -> None:
    residue_mod: int = 250
    sequence_length: int = 250250
    result_mod: int = 10**16
    chunk_size: int = 2500
    workers: int = max(1, os.cpu_count() or 1)
    ranges = list(generate_chunk_ranges(1, sequence_length, chunk_size))
    residue_counts: List[int] = [0] * residue_mod
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(count_residues_in_range, r, residue_mod)
                   for r in ranges]
        for future in tqdm(as_completed(futures), total=len(ranges),
                           desc="Counting residues"):
            counts = future.result()
            for i in range(residue_mod):
                residue_counts[i] += counts[i]
    tasks = [(r, residue_counts[r], result_mod)
             for r in range(residue_mod) if residue_counts[r] > 0]
    polynomials: List[List[int]] = []
    scalar: int = 1
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(compute_residue_polynomial, t) for t in tasks]
        for future in tqdm(as_completed(futures), total=len(tasks),
                           desc="Computing polynomials"):
            res, poly = future.result()
            if poly is None:
                continue
            if res == 0:
                scalar = (scalar * poly[0]) % result_mod
            else:
                polynomials.append(poly)
    final_poly: List[int] = [0] * residue_mod
    final_poly[0] = 1
    for poly in tqdm(polynomials, desc="Performing convolutions"):
        final_poly = modular_polynomial_multiply(final_poly, poly, result_mod)
    if scalar != 1:
        final_poly = [(x * scalar) % result_mod for x in final_poly]
    answer = (final_poly[0] - 1) % result_mod
    print(str(answer).zfill(16))

if __name__ == "__main__":
    main()