# Problem: https://projecteuler.net/problem=20
import math

def main():
    """ Finding the sum of the digits in the number 100! """
    factorial_100 = math.factorial(100)
    sum_of_digits = sum(int(digit) for digit in str(factorial_100))
    print(sum_of_digits)

if __name__ == "__main__":
    main()
