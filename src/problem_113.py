# Problem: https://projecteuler.net/problem=113
from sympy import binomial

def non_bouncy_numbers(digits):
    increasing = binomial(digits + 9, 9) - 1
    decreasing = binomial(digits + 10, 10) - (digits + 1)
    return increasing + decreasing

if __name__ == "__main__":
    digits = 100
    answer = non_bouncy_numbers(digits) - 9 * digits
    print(answer)