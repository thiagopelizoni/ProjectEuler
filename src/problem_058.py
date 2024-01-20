# Problem: https://projecteuler.net/problem=58
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def spiral_primes(limit):
    primes_count = 0
    total_diagonals = 1
    side_length = 1
    number = 1

    while True:
        side_length += 2
        for _ in range(4):
            number += side_length - 1
            if is_prime(number):
                primes_count += 1
        total_diagonals += 4
        if primes_count / total_diagonals < 0.1:
            break

    return side_length

limit = 10
answer = spiral_primes(limit)
print(answer)
