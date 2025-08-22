# Problem: https://projecteuler.net/problem=228
import multiprocessing
from multiprocessing import Pool
from fractions import Fraction
from tqdm import tqdm

def create_set_for_n(n):
    local_set = set()
    for k in range(n):
        fraction = Fraction(k, n)
        local_set.add(fraction)
    return local_set

if __name__ == '__main__':
    starting_n = 1864
    ending_n = 1909
    all_n_values = list(range(starting_n, ending_n + 1))
    number_of_processes = multiprocessing.cpu_count()
    with Pool(number_of_processes) as pool:
        sets_for_each_n = list(tqdm(pool.imap(create_set_for_n, all_n_values), total=len(all_n_values)))
    total_unique_fractions = set()
    for current_set in sets_for_each_n:
        total_unique_fractions.update(current_set)
    number_of_sides = len(total_unique_fractions)
    print(number_of_sides)