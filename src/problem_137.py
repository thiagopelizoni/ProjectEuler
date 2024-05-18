# Problem: https://projecteuler.net/problem=111
import time

from sympy import fibonacci

def main():
    index = 15
    answer = fibonacci(2 * index) * fibonacci(2 * index + 1)

    print(answer)

if __name__ == "__main__":
    main()