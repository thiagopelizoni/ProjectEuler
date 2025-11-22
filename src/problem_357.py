# Problem: https://projecteuler.net/problem=357
import math
import numpy as np
from numba import jit
from tqdm import tqdm

@jit(nopython=True)
def is_valid(n: int, isprime: np.ndarray) -> bool:
    sqrt = int(math.sqrt(n)) + 1
    for d in range(1, sqrt):
        if n % d == 0:
            sum_div = d + n // d
            if sum_div >= len(isprime) or not isprime[sum_div]:
                return False
    return True

def main():
    LIMIT = 100000000
    isprime = np.full(LIMIT + 2, True, dtype=bool)
    isprime[0] = isprime[1] = False
    for i in range(2, int(math.sqrt(LIMIT + 1)) + 1):
        if isprime[i]:
            isprime[i * i : LIMIT + 2 : i] = False
    candidates = np.where(isprime[2:])[0] + 1
    total = 0
    for n in tqdm(candidates):
        if is_valid(n, isprime):
            total += n
    print(total)

if __name__ == "__main__":
    main()