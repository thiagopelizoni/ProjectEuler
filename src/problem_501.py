# Problem: https://projecteuler.net/problem=501

import math
import bisect
from tqdm import tqdm
from math import isqrt


def prime_sieve(n):
    sieve = [True] * (n // 2)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]


def icbrt(n):
    lo = 0
    hi = n // 2 + 2
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


def i4rt(n):
    return isqrt(isqrt(n))


phi_cache = {}

def phi(x, a):
    x = int(x)
    if (x, a) in phi_cache:
        return phi_cache[(x, a)]
    if a == 1:
        result = (x + 1) // 2
    else:
        result = phi(x, a - 1) - phi(x // primes[a - 1], a - 1)
    phi_cache[(x, a)] = result
    return result


pi_cache = {}

def pi(x):
    x = int(x)
    if x in pi_cache:
        return pi_cache[x]
    if x < 2:
        result = 0
    elif x < limit:
        result = bisect.bisect_right(primes, x)
    else:
        a = pi(i4rt(x))
        b = pi(isqrt(x))
        c = pi(icbrt(x))
        result = phi(x, a) + (b + a - 2) * (b - a + 1) // 2
        for i in range(a + 1, b + 1):
            w = x // primes[i - 1]
            b_i = pi(isqrt(w))
            result -= pi(w)
            if i <= c:
                for j in range(i, b_i + 1):
                    result -= pi(w // primes[j - 1]) - (j - 1)
    pi_cache[x] = result
    return result


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 501 by counting the number of positive integers n <= 10^12 that have
    exactly 8 positive divisors.

    Method / Math Rationale
    ----------------------
    Numbers with exactly 8 divisors have prime factorizations of the form p^7, p^3 * q, or p * q * r
    where p, q, r are distinct primes. The function counts the number of such n <= N for each form
    separately using the prime counting function pi(x) implemented using the Meissel-Lehmer algorithm.

    Complexity
    ----------
    The prime counting function is O(n^{2/3} / log^2 n) per call; with memoization, the overall solution
    runs in reasonable time for N = 10^12.

    References
    ----------
    https://projecteuler.net/problem=501
    """
    global limit, primes
    N = 1000000000000
    limit = 10**7
    primes = prime_sieve(limit)

    count_a7 = 0
    for p in primes:
        if p ** 7 > N:
            break
        count_a7 += 1

    count_a3b = 0
    for p in primes:
        p3 = p * p * p
        if p3 > N:
            break
        max_b = N // p3
        num_b = pi(max_b)
        if max_b >= p:
            num_b -= 1
        count_a3b += num_b

    count_abc = 0
    max_a = icbrt(N) + 1
    max_index = bisect.bisect_right(primes, max_a)
    for index_a in tqdm(range(max_index)):
        a = primes[index_a]
        if a * a * a > N:
            continue
        local_count = 0
        for index_b in range(index_a + 1, len(primes)):
            b = primes[index_b]
            max_c = N // (a * b)
            if max_c <= b:
                break
            high = pi(max_c)
            low = index_b + 1
            local_count += high - low
        count_abc += local_count

    total = count_a7 + count_a3b + count_abc
    print(total)


if __name__ == "__main__":
    main()