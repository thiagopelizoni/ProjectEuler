# Problem: https://projecteuler.net/problem=397
from collections import defaultdict
from tqdm import tqdm
import math

def sieve(n):
    spf = list(range(n + 1))
    for i in range(2, int(math.sqrt(n)) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def get_factors(n, spf):
    factors = defaultdict(int)
    while n > 1:
        p = spf[n]
        while n % p == 0:
            factors[p] += 1
            n //= p
    return factors

def generate_divisors(factors):
    primes = list(factors.keys())
    exps = list(factors.values())
    def helper(idx, curr):
        if idx == len(primes):
            yield curr
            return
        p = primes[idx]
        e = exps[idx]
        val = 1
        for i in range(e + 1):
            yield from helper(idx + 1, curr * val)
            val *= p
    return list(helper(0, 1))

def main():
    K = 10**6
    X = 10**9
    spf = sieve(K)
    result = 0
    for k in tqdm(range(1, K + 1)):
        fact_k = get_factors(k, spf)
        fact = defaultdict(int)
        fact[2] = 1 + fact_k[2] * 2 if 2 in fact_k else 1
        for p, e in fact_k.items():
            if p != 2:
                fact[p] = 2 * e
        pos_divs = generate_divisors(fact)
        all_f = set(pos_divs)
        all_f.update(-d for d in pos_divs)
        all_f.discard(0)

        count_a = 0
        for d in all_f:
            s = k - d
            num = k * k + s * k
            if num % d != 0:
                continue
            m = num // d
            if m <= s:
                continue
            lower = max(-X, m - X, s - X)
            upper = (s - 1) // 2
            if lower <= upper:
                count_a += upper - lower + 1

        count_b = 0
        for e in all_f:
            s = e - k
            num = -k * k - s * s
            if num % e != 0:
                continue
            m = num // e
            lower = max(-X, (s - m) // 2 + 1, s - X)
            upper = min((s - 1) // 2, X - m)
            if lower <= upper:
                count_b += upper - lower + 1

        # compute overlap_B = isosceles right at B = |A ∩ C|
        fact_sq = defaultdict(int)
        for p, e in fact_k.items():
            fact_sq[p] = 2 * e
        pos_divs_k2 = generate_divisors(fact_sq)
        overlap_B = 0
        for d in pos_divs_k2:
            q = k * k // d
            l_b = max(-X, (-d // 2) + 1, q - X)
            u_b = min(X, (q - 1) // 2, X - d)
            numerator = (k - d) * (k * k + k * d + d * d)
            denom = 2 * d * (d + k)
            if denom != 0 and numerator % denom == 0:
                b = numerator // denom
                if l_b <= b <= u_b:
                    overlap_B += 1

        # compute overlap_A = isosceles right at A = |B ∩ C|
        overlap_A = 0
        for d in pos_divs_k2:
            q = k * k // d
            l_a = max(-X, q - X)
            u_a = (-d - 1) // 2
            numerator = (k + d) * (k * k - k * d + d * d)
            denom = 2 * d * (k - d)
            if denom != 0 and numerator % denom == 0:
                a = numerator // denom
                if l_a <= a <= u_a:
                    overlap_A += 1

        local = count_a * 2 + count_b - overlap_B - 2 * overlap_A
        result += local
    print(result)

if __name__ == "__main__":
    main()