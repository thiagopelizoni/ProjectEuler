# Problem: https://projecteuler.net/problem=118
from sympy import isprime
from itertools import permutations

digit_list = list(range(1, 10))

def count_prime_sets(start_index, previous_number, digit_permutation):
    if start_index == len(digit_permutation):
        return 1
    else:
        result = 0
        for split in range(start_index + 1, len(digit_permutation) + 1):
            number = int("".join(map(str, digit_permutation[start_index : split])))
            if number > previous_number and isprime(number):
                result += count_prime_sets(split, number, digit_permutation)
        return result

total = 0
for digit_permutation in permutations(digit_list):
    total += count_prime_sets(0, 0, digit_permutation)

if __name__ == "__main__":
    print(str(total))
