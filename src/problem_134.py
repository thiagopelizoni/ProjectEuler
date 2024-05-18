# Problem: https://projecteuler.net/problem=134
import sympy
import itertools

def main():
    result = 0
    primes = list(sympy.primerange(1, 2000000))
    for i in itertools.count(2):
        p = primes[i]
        q = primes[i + 1]
        if p > 1000000:
            break
        k = 1
        while k < p:
            k *= 10
        m = (q - p) * pow(k, -1, q) % q
        result += m * k + p
    return str(result)

if __name__ == "__main__":
    print(main())