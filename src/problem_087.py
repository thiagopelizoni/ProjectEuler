# Problem: https://projecteuler.net/problem=87
from sympy import primerange

LIMIT = 50_000_000

primes_square = [p for p in primerange(1, int(LIMIT ** 0.5) + 1)]
primes_cube = [p for p in primerange(1, int(LIMIT ** (1/3)) + 1)]
primes_fourth_power = [p for p in primerange(1, int(LIMIT ** 0.25) + 1)]

expressible_numbers = set()

for square in primes_square:
    for cube in primes_cube:
        for fourth_power in primes_fourth_power:
            number = square**2 + cube**3 + fourth_power**4
            if number < LIMIT:
                expressible_numbers.add(number)

answer = len(expressible_numbers)
print(answer)
