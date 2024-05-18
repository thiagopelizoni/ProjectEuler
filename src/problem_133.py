# Problem: https://projecteuler.net/problem=133
import sympy

def main():
    primes = list(sympy.primerange(1, 100000))
    result = sum(p for p in primes if p == 2 or p == 5 or not has_divisible_repunit(p))
    return str(result)

def has_divisible_repunit(p):
    return (pow(10, 10**16, p * 9) - 1) // 9 % p == 0

if __name__ == "__main__":
    print(main())