# Problem: https://projecteuler.net/problem=7
from sympy import isprime

def nth_prime(n):
    count = 0
    num = 1
    while count < n:
        num += 1
        if isprime(num):
            count += 1
    return num

if __name__ == "__main__":
    answer = nth_prime(10001)
    print(answer)
