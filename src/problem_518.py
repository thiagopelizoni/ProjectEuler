# Problem: https://projecteuler.net/problem=518
import math
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from tqdm import tqdm

PRIME_ARR = None

def init_pool(shared_arr):
    global PRIME_ARR
    PRIME_ARR = shared_arr

def process_x(x, limit):
    from math import gcd
    np_arr = np.ctypeslib.as_array(PRIME_ARR)
    local_sum = 0
    max_k = (limit - 1) // (x * x)
    for k in range(1, max_k + 1):
        a = k * x * x - 1
        if a >= limit or np_arr[a] == 0:
            continue
        for y in range(1, x):
            if x % 2 == 0 and y % 2 == 0:
                continue
            b = k * x * y - 1
            if b < 2 or b >= limit or np_arr[b] == 0:
                continue
            c = k * y * y - 1
            if c < 2 or c >= limit or np_arr[c] == 0:
                continue
            if gcd(x, y) > 1:
                continue
            local_sum += a + b + c
    return local_sum

def main():
    limit = 10**8
    arr = mp.RawArray('b', limit)
    np_arr = np.ctypeslib.as_array(arr)
    np_arr[:] = 1
    np_arr[0] = 0
    np_arr[1] = 0
    sqrt_lim = int(math.sqrt(limit)) + 1
    for i in range(2, sqrt_lim):
        if np_arr[i]:
            np_arr[i * i : limit : i] = 0
    x_start = 2
    x_end = int(math.sqrt(limit - 1)) + 1
    futures = []
    with ProcessPoolExecutor(initializer=init_pool, initargs=(arr,)) as executor:
        for x in range(x_start, x_end + 1):
            futures.append(executor.submit(process_x, x, limit))
    total = 0
    for future in tqdm(as_completed(futures), total=len(futures)):
        total += future.result()
    print(total)

if __name__ == "__main__":
    main()