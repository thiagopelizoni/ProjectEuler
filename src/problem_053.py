# Problem: https://projecteuler.net/problem=53
from math import factorial

def combinatorial_selections(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def answer(limit):
    count = 0
    for n in range(1, 101):
        for r in range(1, n + 1):
            if combinatorial_selections(n, r) > limit:
                count += 1
    return count

limit = 1_000_000
print(answer(limit))
