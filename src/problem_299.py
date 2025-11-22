# Problem: https://projecteuler.net/problem=299
from math import gcd
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def compute_par_for_m(m, L):
    local_count = 0
    # Compute max_n for this m
    import math
    max_n_float = math.sqrt(L / 2 - m**2) - m if L / 2 > m**2 else 0
    max_n = int(max_n_float) + 1 if max_n_float > 0 else 0
    for n in range(1, max_n + 1):
        if gcd(m, n) == 1:
            c = n * n + 2 * m * m
            f = 2 * m * n
            if gcd(c, f) != 1:
                continue
            s = 2 * (c + f)
            if s >= L:
                continue
            k_max = (L - 1) // s
            local_count += k_max
    return local_count

def main():
    L = 100000000
    count_in = 0
    max_m = int(L**0.5) + 10
    for m in tqdm(range(2, max_m + 1)):
        for n in range(1, m):
            if gcd(m, n) == 1 and (m - n) % 2 == 1:
                p = m * m - n * n
                q = 2 * m * n
                s = p + q
                k_max = (L - 1) // s
                count_in += 2 * k_max
    count_par = 0
    max_m_par = int((L / 2)**0.5) + 10
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_par_for_m, m, L) for m in range(1, max_m_par + 1)]
        for future in tqdm(futures):
            count_par += future.result()
    print(count_in + count_par)

if __name__ == "__main__":
    main()