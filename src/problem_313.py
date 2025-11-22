# Problem: https://projecteuler.net/problem=313
from sympy.ntheory import primerange

def main():
    limit = 1000000
    total = 0
    for p in primerange(2, limit):
        if p == 3:
            total += 2
        else:
            total += (p * p - 1) // 12
    print(total)

if __name__ == "__main__":
    main()