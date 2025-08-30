# Problem: https://projecteuler.net/problem=1
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import cpu_count
from typing import Dict
from tqdm import tqdm

def sum_of_multiples(m: int, limit: int) -> int:
    k = (limit - 1) // m
    return m * k * (k + 1) // 2

def compute(limit: int) -> int:
    terms = ((3, 1), (5, 1), (15, -1))
    total = 0
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        future_to_sign: Dict = {
            executor.submit(sum_of_multiples, m, limit): sign for m, sign in terms
        }
        for future in tqdm(as_completed(future_to_sign), total=len(future_to_sign)):
            total += future_to_sign[future] * future.result()
    return total

if __name__ == "__main__":
    print(compute(1000))
