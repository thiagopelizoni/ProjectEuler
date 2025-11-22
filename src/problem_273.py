# Problem: https://projecteuler.net/problem=273

from concurrent.futures import ProcessPoolExecutor
from math import sqrt
from os import cpu_count
from tqdm import tqdm
from typing import List

from sympy.ntheory import primerange

def compute_sum_chunk(start: int, end: int, us: List[int], vs: List[int]) -> int:
    total = 0
    num_primes = len(us)
    base = 3
    for config_id in tqdm(range(start, end)):
        re = 1
        im = 0
        temp = config_id
        for j in range(num_primes):
            choice = temp % base
            temp //= base
            if choice == 0:
                continue
            u = us[j]
            v = vs[j]
            if choice == 1:
                new_re = re * u - im * v
                new_im = re * v + im * u
            else:
                new_re = re * u + im * v
                new_im = -re * v + im * u
            re = new_re
            im = new_im
        min_ab = min(abs(re), abs(im))
        total += min_ab
    return total

def main() -> None:
    primes = [p for p in primerange(5, 150) if p % 4 == 1]
    us: List[int] = []
    vs: List[int] = []
    for p in primes:
        for uu in range(1, int(sqrt(p)) + 1):
            vv_sq = p - uu * uu
            vv = int(sqrt(vv_sq))
            if vv * vv == vv_sq:
                us.append(uu)
                vs.append(vv)
                break
    num_primes = len(primes)
    total_configs = 3**num_primes
    num_cpus = cpu_count() or 1
    chunk_size = (total_configs // num_cpus) + 1
    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(num_cpus):
            start = i * chunk_size
            end = min(start + chunk_size, total_configs)
            if start >= end:
                continue
            futures.append(
                executor.submit(compute_sum_chunk, start, end, us, vs)
            )
        partial_sums = [f.result() for f in futures]
    total_sum_min = sum(partial_sums)
    print(total_sum_min // 2)

if __name__ == "__main__":
    main()