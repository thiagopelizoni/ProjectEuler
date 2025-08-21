# Problem: https://projecteuler.net/problem=226
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np


def compute_blancmange_chunk(x_values):
    blancmange = np.zeros_like(x_values)
    fractional_parts = x_values % 1.0
    scale_factor = 1.0

    for _ in range(60):
        sawtooth = np.minimum(fractional_parts, 1.0 - fractional_parts)
        blancmange += sawtooth * scale_factor
        scale_factor *= 0.5
        fractional_parts = (2.0 * fractional_parts) % 1.0

    return blancmange


if __name__ == "__main__":
    number_of_points = 2 ** 26
    x_values = np.linspace(0.0, 0.5, number_of_points)
    cpu_count = multiprocessing.cpu_count()
    x_chunks = np.array_split(x_values, cpu_count)

    with Pool(cpu_count) as pool:
        blancmange_chunks = list(
            tqdm(pool.imap(compute_blancmange_chunk, x_chunks), total=len(x_chunks))
        )

    blancmange_values = np.concatenate(blancmange_chunks)

    dx_to_center_squared = (0.25 - x_values) ** 2
    half_circle_radius_squared = 0.0625
    radial_discriminant = np.maximum(0.0, half_circle_radius_squared - dx_to_center_squared)
    radial_distance = np.sqrt(radial_discriminant)

    circle_lower_y = 0.5 - radial_distance
    circle_upper_y = 0.5 + radial_distance

    integrand = np.maximum(0.0, np.minimum(circle_upper_y, blancmange_values) - circle_lower_y)
    area = np.trapezoid(integrand, x_values)

    print(f"{area:.8f}")