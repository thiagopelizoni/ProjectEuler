# Problem: https://projecteuler.net/problem=482
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations_with_replacement
from math import gcd, isqrt
from tqdm import tqdm


def process_task(task):
    leg1, leg2, start_k, end_k = task
    pairs = [(k * leg1, k * leg2) for k in range(start_k, end_k + 1)] + \
            [(k * leg2, k * leg1) for k in range(start_k, end_k + 1)]
    return pairs


def main():
    P = 10**7
    max_leg = P // 2 + 1
    m_limit = int((2 * max_leg)**0.5) + 2

    primitives = []
    for m in range(2, m_limit + 1):
        for n in range(1, m):
            if (m - n) % 2 == 1 and gcd(m, n) == 1:
                leg1 = m**2 - n**2
                leg2 = 2 * m * n
                primitives.append((leg1, leg2, max_leg))

    tasks = []
    chunk_size = 10000
    for leg1, leg2, max_leg in primitives:
        max_k = max_leg // max(leg1, leg2)
        if max_k == 0:
            continue
        num_chunks = (max_k - 1) // chunk_size + 1
        for i in range(num_chunks):
            start = i * chunk_size + 1
            end = min((i + 1) * chunk_size, max_k)
            tasks.append((leg1, leg2, start, end))

    partners = defaultdict(list)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in tqdm(as_completed(futures), total=len(futures)):
            local_pairs = future.result()
            for r, x in local_pairs:
                partners[r].append(x)

    total = 0
    rs = sorted(partners)
    for r in tqdm(rs):
        xs = sorted(set(partners[r]))
        n_xs = len(xs)
        if n_xs < 3:
            continue
        for x, y, z in combinations_with_replacement(xs, 3):
            s = x + y + z
            p = 2 * s
            if p > P:
                continue
            if x * y * z == r**2 * s:
                d_a = isqrt(r**2 + x**2)
                d_b = isqrt(r**2 + y**2)
                d_c = isqrt(r**2 + z**2)
                total += p + d_a + d_b + d_c

    print(total)


if __name__ == "__main__":
    main()