# Problem: https://projecteuler.net/problem=266
import bisect
import math
from tqdm import tqdm
from sympy.ntheory import primerange

primes = list(primerange(2, 190))
p = 1
for pr in primes:
    p *= pr

half = len(primes) // 2
group_a = primes[:half]
group_b = primes[half:]

def gen_prods(group):
    prods = [1]
    for pr in group:
        prods += [x * pr for x in prods]
    return prods

list_a = gen_prods(group_a)
list_b = gen_prods(group_b)
list_b.sort()

max_m = 0
for a in tqdm(list_a):
    div = a ** 2
    if div > p:
        continue
    floor_div = p // div
    upper = math.isqrt(floor_div)
    idx = bisect.bisect_right(list_b, upper)
    if idx > 0:
        b = list_b[idx - 1]
        cand = a * b
        if cand > max_m:
            max_m = cand

print(max_m % (10 ** 16))