# Problem: https://projecteuler.net/problem=27

from sympy import isprime

def quadratic_primes(a, b):
    n = 0
    while True:
        if not isprime(n**2 + a * n + b):
            return n
        n += 1

def main():
    max_n = 0
    answer = 0

    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            n = quadratic_primes(a, b)
            if n > max_n:
                max_n = n
                answer = a * b

    print(answer)

if __name__ == "__main__":
    main()
