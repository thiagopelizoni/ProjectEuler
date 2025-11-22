# Problem: https://projecteuler.net/problem=455
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def find_fixed_point(n, modulo=1000000000):
    exponent = n
    while True:
        next_exp = pow(n, exponent, modulo)
        if next_exp == 0 or next_exp == exponent:
            return next_exp
        exponent = next_exp

def main():
    limit = 1000000
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(find_fixed_point, range(2, limit + 1)), total=limit - 1))
    print(sum(results))

if __name__ == "__main__":
    main()