# Problem: https://projecteuler.net/problem=342
import math
from tqdm import tqdm

def get_spf(limit):
    spf = list(range(limit + 1))
    for i in range(2, int(math.sqrt(limit)) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize(n, spf):
    factors = {}
    while n > 1:
        p = spf[n]
        exp = 0
        while n % p == 0:
            n //= p
            exp += 1
        factors[p] = exp
    return factors

def find_max_k(nlim):
    max_n2 = (nlim - 1) ** 2
    low = 1
    high = 10 ** 7
    while low <= high:
        mid = (low + high) // 2
        if mid ** 3 <= max_n2:
            low = mid + 1
        else:
            high = mid - 1
    return high

def main():
    nlim = 10 ** 10
    M = find_max_k(nlim)
    spf = get_spf(M + 1)
    total = 0
    for i in tqdm(range(2, M + 1)):
        factors = factorize(i, spf)
        primes = sorted(factors.keys())
        t = i ** 3
        check = True
        for q in reversed(primes):
            if t % q != 0:
                continue
            if t % (q - 1) != 0:
                check = False
                break
            t = (t * q) // (q - 1)
        if not check:
            continue
        nn = math.isqrt(t)
        if nn * nn == t and 1 < nn < nlim:
            total += nn
    print(total)

if __name__ == "__main__":
    main()