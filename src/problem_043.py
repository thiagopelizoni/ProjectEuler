# Problem: https://projecteuler.net/problem=43
from itertools import permutations

def has_special_property(num_str):
    primes = [2, 3, 5, 7, 11, 13, 17]
    return all(int(num_str[i + 1:i + 4]) % primes[i] == 0 for i in range(7))

def answer():
    total_sum = 0
    for p in permutations('0123456789'):
        num_str = ''.join(p)
        if has_special_property(num_str):
            total_sum += int(num_str)
    return total_sum

print(answer())
