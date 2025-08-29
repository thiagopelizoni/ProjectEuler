# Problem: https://projecteuler.net/problem=258
import numpy as np
import os

from tqdm import tqdm

MODULUS = 20092010
K_SIZE = 2000
TARGET_N = 10**18
EXPONENT = TARGET_N - K_SIZE + 1
DTYPE = np.int64


def configure_environment_for_parallelism():
    try:
        cpu_count = os.cpu_count()
        if cpu_count:
            num_threads = str(cpu_count)
            if "OMP_NUM_THREADS" not in os.environ:
                os.environ["OMP_NUM_THREADS"] = num_threads
            if "MKL_NUM_THREADS" not in os.environ:
                os.environ["MKL_NUM_THREADS"] = num_threads
            if "OPENBLAS_NUM_THREADS" not in os.environ:
                os.environ["OPENBLAS_NUM_THREADS"] = num_threads
    except Exception:
        pass


def reduce_polynomial_modulo(polynomial, k_size, modulus):
    degree = len(polynomial) - 1
    if degree < k_size:
        return polynomial

    for i in range(degree, k_size - 1, -1):
        coefficient = polynomial[i]
        
        if coefficient != 0:
            polynomial[i - k_size + 1] = (
                polynomial[i - k_size + 1] + coefficient
            ) % modulus

            polynomial[i - k_size] = (
                polynomial[i - k_size] + coefficient
            ) % modulus

    return polynomial[:k_size]


def calculate_polynomial_power_mod(exponent, k_size, modulus):
    if k_size < 1:
        return np.array([], dtype=DTYPE)

    base_poly = np.zeros(k_size, dtype=DTYPE)
    if k_size > 1:
        base_poly[1] = 1

    result_poly = np.zeros(k_size, dtype=DTYPE)
    result_poly[0] = 1

    num_iterations = exponent.bit_length()
    
    current_exponent = exponent
    
    description = "Polynomial Exponentiation"
    with tqdm(total=num_iterations, desc=description) as progress_bar:
        while current_exponent > 0:
            if current_exponent % 2 == 1:
                product = np.convolve(result_poly, base_poly)
                product_mod = product % modulus
                result_poly = reduce_polynomial_modulo(
                    product_mod, k_size, modulus
                )

            current_exponent //= 2
            
            if current_exponent > 0:
                squared_base = np.convolve(base_poly, base_poly)
                squared_base_mod = squared_base % modulus
                base_poly = reduce_polynomial_modulo(
                    squared_base_mod, k_size, modulus
                )
            
            progress_bar.update(1)

    return result_poly


def solve():
    configure_environment_for_parallelism()

    if K_SIZE < 1:
        return 0

    remainder_coefficients = calculate_polynomial_power_mod(
        EXPONENT, K_SIZE, MODULUS
    )

    r_0 = remainder_coefficients[0]

    if K_SIZE > 1:
        sum_of_other_coeffs = np.sum(
            remainder_coefficients[1:]
        ) % MODULUS
    else:
        sum_of_other_coeffs = 0

    result_g_n = (r_0 + 2 * sum_of_other_coeffs) % MODULUS

    return int(result_g_n)

if __name__ == '__main__':
    print(solve())