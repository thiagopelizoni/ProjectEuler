# Problem: https://projecteuler.net/problem=183
import math
import multiprocessing as mp
from tqdm import tqdm

def find_optimal_k(n_value):
    current_k = 2
    previous_log_product = 2 * (math.log(n_value) - math.log(2))
    while True:
        next_k = current_k + 1
        current_log_product = next_k * (math.log(n_value) - math.log(next_k))
        if current_log_product <= previous_log_product:
            return current_k
        previous_log_product = current_log_product
        current_k = next_k

def is_terminating(m_value):
    temp = m_value
    while temp % 2 == 0:
        temp //= 2
    while temp % 5 == 0:
        temp //= 5
    return temp == 1

def compute_d(n_value):
    k = find_optimal_k(n_value)
    d = math.gcd(n_value, k)
    m = k // d
    if is_terminating(m):
        return -n_value
    return n_value

def compute_sum_in_range(start_n, end_n):
    local_sum = 0
    for current_n in tqdm(range(start_n, end_n + 1)):
        local_sum += compute_d(current_n)
    return local_sum

if __name__ == "__main__":
    start_n = 5
    end_n = 10000
    num_cores = mp.cpu_count()
    chunk_size = (end_n - start_n + 1) // num_cores
    range_list = []
    current_start = start_n
    for core in range(num_cores):
        current_end = current_start + chunk_size - 1
        if core == num_cores - 1:
            current_end = end_n
        range_list.append((current_start, current_end))
        current_start = current_end + 1

    with mp.Pool(num_cores) as pool:
        results = pool.starmap(compute_sum_in_range, range_list)

    total = sum(results)
    print(total)