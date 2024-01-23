# Problem: https://projecteuler.net/problem=94
import math
from collections import defaultdict

# Function to calculate the sum of proper divisors of a number
def sum_of_divisors(n):
    total = 1
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

# Function to find the amicable chain
def find_amicable_chain(limit):
    divisor_sum = [0] * (limit + 1)
    for i in range(2, limit + 1):
        divisor_sum[i] = sum_of_divisors(i)

    longest_chain_length = 0
    smallest_member = 0

    for i in range(2, limit + 1):
        chain = []
        current = i
        while divisor_sum[current] < limit:
            current = divisor_sum[current]
            if current in chain:
                # Found a cycle
                start_index = chain.index(current)
                chain_length = len(chain) - start_index
                if chain_length > longest_chain_length:
                    longest_chain_length = chain_length
                    smallest_member = min(chain[start_index:])
                break
            chain.append(current)

    return smallest_member

limit = 10**6
answer = find_amicable_chain(limit)
print(answer)
