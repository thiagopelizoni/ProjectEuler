# Problem: https://projecteuler.net/problem=80
import decimal
import math

decimal.getcontext().prec = 102

def is_square(integer):
    root = math.isqrt(integer)
    return integer == root * root

def digital_sum_of_sqrt(n):
    # Skip perfect squares, since their square root is an integer, not irrational
    if is_square(n):
        return 0
    # Calculate the square root with high precision
    sqrt_n = decimal.Decimal(n).sqrt()
    # Convert to string, remove the point and take the first 100 decimals
    digits = str(sqrt_n).replace('.', '')[:100]
    # Return the sum of these digits as integers
    return sum(int(digit) for digit in digits)

if __name__ == "__main__":
    answer = sum(digital_sum_of_sqrt(i) for i in range(1, 101))
    print(answer)
