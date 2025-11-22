# Problem: https://projecteuler.net/problem=346
import math
from tqdm import tqdm

def main():
    limit = 10**12
    repunits = set()
    result = 1
    d = 4 * limit - 3
    max_b_float = (-1 + math.sqrt(d)) / 2
    max_base = int(max_b_float)
    for base in tqdm(range(2, max_base + 1)):
        n = 1 + base
        exp = 2
        while True:
            to_add = base ** exp
            n += to_add
            if n >= limit:
                break
            if n not in repunits:
                repunits.add(n)
                result += n
            exp += 1
    print(result)

if __name__ == "__main__":
    main()