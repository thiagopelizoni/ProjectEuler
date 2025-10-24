# Problem: https://projecteuler.net/problem=451
from concurrent.futures import ProcessPoolExecutor
from itertools import product
from tqdm import tqdm

LIMIT = 20000000

def compute_spf():
    spf = list(range(LIMIT + 1))
    for i in range(2, int(LIMIT**0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, LIMIT + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

SPF = compute_spf()

def get_factors(n):
    factors = []
    while n > 1:
        p = SPF[n]
        e = 0
        mod = 1
        while n % p == 0:
            n //= p
            e += 1
            mod *= p
        factors.append((p, e, mod))
    return factors

def get_local_sols(p, e, mod):
    if p == 2:
        if e == 1:
            return [1]
        elif e == 2:
            return [1, 3]
        else:
            half = mod // 2
            return [1, mod - 1, half - 1, half + 1]
    else:
        return [1, mod - 1]

def crt(as_, ms_, n):
    x = 0
    for a, m in zip(as_, ms_):
        M_i = n // m
        inv = pow(M_i, -1, m)
        x += a * M_i * inv
        x %= n
    return x

def compute_I(n):
    factors = get_factors(n)
    locals_list = []
    mods = []
    for p, e, mod in factors:
        locals_list.append(get_local_sols(p, e, mod))
        mods.append(mod)
    max_m = 0
    for tup in product(*locals_list):
        x = crt(tup, mods, n)
        if x > max_m and x < n - 1:
            max_m = x
    return max_m

def sum_I(start, end):
    s = 0
    for n in range(max(start, 3), end + 1):
        s += compute_I(n)
    return s

def main():
    """
    Purpose
    -------
    Computes the sum of I(n) for 3 <= n <= 2*10^7, where I(n) is the largest m < n-1 such that
    m^2 ≡ 1 mod n.

    Method / Math Rationale
    ------------------------
    For each n, factorize using precomputed smallest prime factor sieve, get local solutions to
    x^2 ≡ 1 mod p^e for each prime power p^e dividing n, then use Cartesian product to get all
    combinations, compute each global x using Chinese Remainder Theorem, and find the maximum x < n-1.

    Complexity
    ----------
    O(LIMIT log log LIMIT for sieve + sum over n of 2^{omega(n)} * omega(n) for combinations and CRT),
    parallelized over chunks of n using ProcessPoolExecutor.

    References
    ----------
    https://projecteuler.net/problem=451
    """
    chunk_size = 100000
    chunks = list(range(1, LIMIT + 1, chunk_size))
    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(len(chunks) - 1):
            start = chunks[i]
            end = chunks[i + 1] - 1
            futures.append(executor.submit(sum_I, start, end))
        if chunks[-1] <= LIMIT:
            futures.append(executor.submit(sum_I, chunks[-1], LIMIT))
        total = 0
        for f in tqdm(futures):
            total += f.result()
    print(total)

if __name__ == "__main__":
    main()