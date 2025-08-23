# Problem: https://projecteuler.net/problem=237
import numpy as np
from tqdm import tqdm

modulus = 100000000
large_n = 10 ** 12

def matrix_power(base_matrix, exponent, mod_value):
    matrix_size = base_matrix.shape[0]
    result_matrix = np.eye(matrix_size, dtype=object)
    progress_bar = tqdm(total=exponent.bit_length(), desc="Matrix exponentiation progress")
    while exponent > 0:
        if exponent % 2 == 1:
            result_matrix = np.dot(result_matrix, base_matrix) % mod_value
        base_matrix = np.dot(base_matrix, base_matrix) % mod_value
        exponent //= 2
        progress_bar.update(1)
    progress_bar.close()
    return result_matrix

transition_matrix = np.array([
    [2, 2, modulus - 2, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
], dtype=object)

initial_vector = np.array([[8], [4], [1], [1]], dtype=object)

if large_n <= 4:
    base_cases = [0, 1, 1, 4, 8]
    print(base_cases[large_n] % modulus)
else:
    powered_matrix = matrix_power(transition_matrix, large_n - 4, modulus)
    result_vector = np.dot(powered_matrix, initial_vector) % modulus
    print(result_vector[0][0])