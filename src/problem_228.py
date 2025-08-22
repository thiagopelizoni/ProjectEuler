# Problem: https://projecteuler.net/problem=228
import multiprocessing
from multiprocessing import Pool
from fractions import Fraction
from tqdm import tqdm


def create_set_for_n(n):
    fraction_set = set()
    for numerator in range(n):
        value = Fraction(numerator, n)
        fraction_set.add(value)
    return fraction_set


if __name__ == "__main__":
    start_n = 1864
    end_n = 1909
    n_values = list(range(start_n, end_n + 1))
    cpu_count = multiprocessing.cpu_count()

    with Pool(cpu_count) as pool:
        sets_per_n = list(
            tqdm(pool.imap(create_set_for_n, n_values), total=len(n_values))
        )

    unique_fractions = set()
    for fraction_set in sets_per_n:
        unique_fractions.update(fraction_set)

    total_sides = len(unique_fractions)
    print(total_sides)