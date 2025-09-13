# Problem: https://projecteuler.net/problem=309
import math
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def factorize(n, spf):
    if n <= 1:
        return {}
    fact = defaultdict(int)
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        fact[p] = e
    return fact

def get_all_divisors(fact):
    if not fact:
        return [1]
    primes = list(fact)
    exps = [fact[p] for p in primes]
    divisors = [1]
    for i in range(len(primes)):
        new_divs = []
        p = primes[i]
        e = exps[i]
        mul = 1
        for j in range(e + 1):
            for d in divisors:
                new_divs.append(d * mul)
            mul *= p
        divisors = new_divs
    return divisors

def compute_count_for_h(h, spf, M):
    count = 0
    fact_h = factorize(h, spf)
    fact_h2 = {p: 2 * e for p, e in fact_h.items()}
    divs = get_all_divisors(fact_h2)
    u_list = [d for d in divs if d <= h]
    for u in u_list:
        if u >= h:
            continue
        num = (h - u) * (h + u) ** 3
        u2 = u ** 2
        if num % u2 != 0:
            continue
        D = num // u2
        if D >= M ** 2:
            continue
        fact_hmu = factorize(h - u, spf)
        fact_hpu = factorize(h + u, spf)
        fact_u = factorize(u, spf)
        fact_D = defaultdict(int)
        for p, e in fact_hmu.items():
            fact_D[p] += e
        for p, e in fact_hpu.items():
            fact_D[p] += 3 * e
        for p, e in fact_u.items():
            fact_D[p] -= 2 * e
        skip = False
        for e in fact_D.values():
            if e < 0:
                skip = True
                break
        if skip:
            continue
        divs_D = get_all_divisors(fact_D)
        divs_D.sort()
        sq_D = math.isqrt(D)
        for f in divs_D:
            if f > sq_D:
                break
            g = D // f
            if f >= g or (f % 2 != g % 2):
                continue
            x = (g - f) // 2
            y = (g + f) // 2
            if not (0 < x < y < M):
                continue
            A = h + u
            temp = x ** 2 - A ** 2
            if temp <= 0:
                continue
            w = math.isqrt(temp)
            if w ** 2 == temp and w > 0:
                count += 1
    return count

def process_range(start, end, spf, M):
    count = 0
    for h in range(start, end):
        count += compute_count_for_h(h, spf, M)
    return count

def main():
    """
    Purpose
    Solve Project Euler problem 309 by counting the number of integer triplets (x, y, h)
    where 0 < x < y < 1000000 such that the street width w is a positive integer in the
    crossing ladders problem.

    Method / Math Rationale
    For each h, find divisors u of h^2 with u <= h. Compute A = h + u, v = h^2 / u,
    B = h + v. Derive D = (h - u) * (h + u)^3 / u^2 ensuring it is integer. Skip if
    D >= 1000000^2. Factor D using factorizations of (h - u), (h + u), and u. Generate
    all divisors of D. For each pair f < g = D / f with f <= isqrt(D) and f, g same
    parity, compute x = (g - f)/2, y = (g + f)/2. If 0 < x < y < 1000000 and x^2 -
    A^2 is a positive perfect square, count the triplet.

    Complexity
    Precompute SPF: O(MAX log log MAX). Per h: O(d(h^2) * (log terms + d(D))) with
    d(D) up to ~10^5 in worst cases, but filtered; total feasible with parallelism over
    chunks of h range.

    References
    https://projecteuler.net/problem=309
    """
    M = 1000000
    MAX_N = 2 * M + 10
    spf = list(range(MAX_N + 1))
    for i in range(2, math.isqrt(MAX_N) + 1):
        if spf[i] == i:
            for j in range(i * i, MAX_N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    num_workers = cpu_count()
    chunk_size = (M - 1) // num_workers + 1
    ranges = []
    for i in range(num_workers):
        start = i * chunk_size + 1
        end = min((i + 1) * chunk_size + 1, M)
        if start < end:
            ranges.append((start, end))
    total = 0
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_range, start, end, spf, M)
                   for start, end in ranges]
        for future in tqdm(as_completed(futures), total=len(ranges), file=sys.stderr):
            total += future.result()
    print(total)

if __name__ == "__main__":
    main()