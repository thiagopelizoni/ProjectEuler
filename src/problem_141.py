# Problem: https://projecteuler.net/problem=141
import math
from math import gcd, isqrt

def is_perfect_square(number):
    return isqrt(number) ** 2 == number

limit = 1000000000000
sum_of_progressive_squares = 0
progressive_squares_set = set()
max_y_value = 3000
max_x_value = 300000

for y_value in range(1, max_y_value + 1):
    max_x_for_y = int((limit / y_value) ** (1 / 3)) + 100

    for x_value in range(y_value + 1, max_x_for_y + 1):
        if gcd(x_value, y_value) != 1:
            continue

        s_value = 1

        while True:
            temp = s_value * (x_value ** 3) + y_value

            n_value = s_value * y_value * temp

            if n_value >= limit:
                break

            if is_perfect_square(n_value):
                progressive_squares_set.add(n_value)

            s_value += 1

if __name__ == "__main__":
    answer = sum(progressive_squares_set)
    print(answer)