# Problem: https://projecteuler.net/problem=108
import numpy as np
from sympy import divisors

def count_solutions(n):
    d = len(divisors(n**2))
    return (d + 1) // 2

def main():
    target_solutions = 1000
    n = 1

    while True:
        if count_solutions(n) > target_solutions:
            print(n)
            break
        n += 1

if __name__ == "__main__":
    main()
