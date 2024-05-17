# Problem: https://projecteuler.net/problem=119
import sympy

def digital_sum(n):
    return sum(map(int, str(n)))

results = []
for base in range(2, 100):
    for exp in range(2, 20):
        num = base ** exp
        if digital_sum(num) == base and num > 9:
            results.append(num)

results.sort()
print(results[29])