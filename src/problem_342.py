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
    """
    Purpose
    -------
    Compute the sum of all integers n where 1 < n < 10^10 such that Euler's totient function
    applied to n squared, phi(n^2), is a perfect cube.

    Method / Math Rationale
    -----------------------
    Iterate over possible k from 2 to the maximum where k^3 <= (10^10 - 1)^2. For each k,
    factorize k to get the distinct primes dividing k^3. Starting with t = k^3, process
    each prime q from largest to smallest: if t is divisible by q, check if divisible by
    (q-1); if not, fail; else update t to t * q / (q-1). If successful, check if the
    final t is a perfect square, compute n = sqrt(t), and if 1 < n < 10^10, add n to
    the sum. This effectively inverts the totient computation for squares whose totient
    is a cube.

    Complexity
    ----------
    O(M log M) for sieving smallest prime factors up to M ~ 4.64e6, plus O(M * d * log(C))
    where d is the number of distinct primes (small), C = k^3 ~ 10^20, for modular and
    division operations on big integers.

    References
    ----------
    https://projecteuler.net/problem=342
    Algorithm inspired by Mathematica code from https://www.tapatalk.com/groups/eulersolutionsfr/problem-342-t156.html
    """
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