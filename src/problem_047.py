# Problem: https://projecteuler.net/problem=47
from collections import defaultdict

def prime_factors(n):
    factors = defaultdict(int)
    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors[i] += 1
            n //= i
    if n > 2:
        factors[n] += 1
    return factors

def answer():
    consecutive = 0
    num = 2
    while True:
        if len(prime_factors(num)) == 4:
            consecutive += 1
            if consecutive == 4:
                return num - 3
        else:
            consecutive = 0
        num += 1

print(answer())
