# Problem: https://projecteuler.net/problem=379
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from tqdm import tqdm
from math import isqrt


def sum_floor(k, l, r):
    if l > r:
        return 0
    res = 0
    while l <= r:
        if k // l == 0:
            break
        rr = min(r, k // (k // l))
        res += (rr - l + 1) * (k // l)
        l = rr + 1
    return res


def _gen_divisors(primes, factors, idx, current, out):
    """
    Recursive helper to enumerate all divisors of a product described
    by `factors`.
    """
    if idx == len(primes):
        out.append(current)
        return

    p = primes[idx]
    pow_p = 1

    # Case: exponent 0 for prime p
    _gen_divisors(primes, factors, idx + 1, current, out)

    # Cases: exponent 1..factors[p] for prime p
    for _ in range(factors[p]):
        pow_p *= p
        _gen_divisors(primes, factors, idx + 1, current * pow_p, out)


def get_divisors(num, spf):
    if num == 1:
        return [1]

    # Factorisation
    factors = {}
    mm = num
    while mm > 1:
        p = spf[mm]
        exp = 0
        while mm % p == 0:
            mm //= p
            exp += 1
        factors[p] = exp

    # Generate divisors
    res = []
    primes = list(factors.keys())
    _gen_divisors(primes, factors, 0, 1, res)
    res.sort()

    return res


def compute_for_i(i, spf, n, mu):
    divs = get_divisors(i, spf)
    s = 0
    for d in divs:
        m = mu[d]
        if m == 0:
            continue
        l = (i + 1 + d - 1) // d
        r = (n // i) // d
        if l > r:
            continue
        k = n // (i * d)
        s += m * sum_floor(k, l, r)
    return s


def main():
    n = 10**12
    sq = isqrt(n)
    max_s = sq + 10
    spf = [0] * (max_s + 1)
    for i in range(2, max_s + 1):
        if spf[i] == 0:
            spf[i] = i
            for j in range(i * i, max_s + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    mu = [0] * (max_s + 1)
    mu[1] = 1
    for i in range(2, max_s + 1):
        p = spf[i]
        if (i // p) % p == 0:
            mu[i] = 0
        else:
            mu[i] = -mu[i // p]
    ans = n
    func = partial(compute_for_i, spf=spf, n=n, mu=mu)
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(func, range(1, sq + 1), chunksize=1000), total=sq))
    ans += sum(results)
    print(ans)


if __name__ == "__main__":
    main()