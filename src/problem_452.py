# Problem: https://projecteuler.net/problem=452
from concurrent.futures import ProcessPoolExecutor
from math import factorial
from tqdm import tqdm

def find_max_y(limit, exp):
    if limit < 1:
        return 0
    low = 1
    high = 2
    while high ** exp <= limit:
        high *= 2
    while low < high:
        mid = (low + high + 1) // 2
        if mid ** exp <= limit:
            low = mid
        else:
            high = mid - 1
    return low

def get_sum(remaining_k, current_prod, current_min, current_accum, current_mult, m, MOD, inv_fact):
    if remaining_k == 0:
        if current_mult == 0:
            return current_accum % MOD
        else:
            return (current_accum * inv_fact[current_mult]) % MOD
    sumv = 0
    max_y = m // current_prod
    if max_y < current_min:
        return 0
    # add same if possible
    if current_mult > 0:
        new_prod = current_prod * current_min
        if new_prod <= m:
            sumv = (sumv + get_sum(remaining_k - 1, new_prod, current_min, current_accum, current_mult + 1, m, MOD, inv_fact)) % MOD
    # add new y
    start_y = current_min if current_mult == 0 else current_min + 1
    if start_y > max_y:
        return sumv % MOD
    # effective max
    limit_remaining = m // current_prod
    max_possible_y = find_max_y(limit_remaining, remaining_k)
    effective_max = min(max_y, max_possible_y)
    if effective_max < start_y:
        return sumv % MOD
    if remaining_k == 1:
        new_accum = current_accum if current_mult == 0 else (current_accum * inv_fact[current_mult]) % MOD
        number = effective_max - start_y + 1
        sumv = (sumv + new_accum * number) % MOD
    else:
        for y in range(start_y, effective_max + 1):
            new_prod = current_prod * y
            new_accum = current_accum if current_mult == 0 else (current_accum * inv_fact[current_mult]) % MOD
            sumv = (sumv + get_sum(remaining_k - 1, new_prod, y, new_accum, 1, m, MOD, inv_fact)) % MOD
    return sumv % MOD

def main():

    m = 10**9
    n = 10**9
    MOD = 1234567891
    MAX_S = 30

    fact = [1] * (MAX_S + 1)
    for i in range(1, MAX_S + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [pow(f, MOD - 2, MOD) for f in fact]

    p = [1] * (MAX_S + 1)
    for s in range(1, MAX_S + 1):
        p[s] = p[s - 1] * (n - s + 1) % MOD

    total = 1  # s=0

    with ProcessPoolExecutor() as executor:
        futures = []
        for s in range(1, MAX_S + 1):
            futures.append(executor.submit(get_sum, s, 1, 2, 1, 0, m, MOD, inv_fact))
        for future in tqdm(futures):
            sum_inv = future.result()
            s = futures.index(future) + 1
            total = (total + p[s] * sum_inv) % MOD
    print(total)

if __name__ == "__main__":
    main()