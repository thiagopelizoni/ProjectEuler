# Problem: https://projecteuler.net/problem=343
from concurrent.futures import ProcessPoolExecutor
from sympy.ntheory import factorint
from tqdm import tqdm

def compute_f(k):
    a = k + 1
    factors_a = factorint(a)
    lpf_a = max(factors_a.keys())
    b = k * k - k + 1
    factors_b = factorint(b)
    lpf_b = max(factors_b.keys()) if factors_b else 0
    max_lpf = max(lpf_a, lpf_b)
    return max_lpf - 1

def main():
    N = 2000000
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(compute_f, range(1, N + 1)), total=N))
    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()