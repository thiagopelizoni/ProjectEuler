# Problem: https://projecteuler.net/problem=417
import math
from math import gcd
from tqdm import tqdm

def build_spf(N):
    spf = list(range(N + 1))
    for i in range(2, int(math.sqrt(N)) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factor(num, spf):
    factors = {}
    while num > 1:
        p = spf[num]
        e = 0
        while num % p == 0:
            num //= p
            e += 1
        factors[p] = e
    return factors

def compute_order(base, mod, spf):
    phi = mod - 1
    fact = factor(phi, spf)
    d = phi
    for q, e in fact.items():
        for _ in range(e):
            if pow(base, d // q, mod) == 1:
                d //= q
            else:
                break
    return d

def compute_order_pk(base, p, k, spf):
    d = compute_order(base, p, spf)
    current_d = d
    current_mod = p
    for lev in range(1, k):
        current_mod *= p
        if pow(base, current_d, current_mod) != 1:
            current_d *= p
    return current_d

def compute_order10(m, spf):
    facts = factor(m, spf)
    ord_m = 1
    for p, k in facts.items():
        d_pk = compute_order_pk(10, p, k, spf)
        ord_m = ord_m * d_pk // gcd(ord_m, d_pk)
    return ord_m

def main():
    N = 100000000
    spf = build_spf(N)
    ms = [m for m in range(2, N + 1) if m % 2 != 0 and m % 5 != 0]
    orders = list(tqdm(map(lambda m: compute_order10(m, spf), ms),
                        total=len(ms)))
    S = [0] * (N + 1)
    for m, o in zip(ms, orders):
        S[m] = o
    prefix = [0] * (N + 1)
    for i in range(1, N + 1):
        prefix[i] = prefix[i - 1] + S[i]
    total = 0
    max_log2 = 0
    while (1 << max_log2) <= N:
        max_log2 += 1
    max_log2 -= 1
    max_log5 = 0
    while 5 ** max_log5 <= N:
        max_log5 += 1
    max_log5 -= 1
    for a in range(max_log2 + 1):
        pow2 = 1 << a
        pow5 = 1
        for b in range(max_log5 + 1):
            k = pow2 * pow5
            if k > N:
                break
            total += prefix[N // k]
            pow5 *= 5
    print(total)

if __name__ == "__main__":
    main()