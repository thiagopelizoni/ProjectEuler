# Problem: https://projecteuler.net/problem=110
from sympy import primerange, Integer

lid = 12
target = 4000000
top = 4

def evaluate(factors):
    result = Integer(1)
    for prime, exponent in factors:
        if exponent > 0:
            result *= prime ** exponent
    return result

def solns(factors):
    total = 1
    for _, exponent in factors:
        total *= 1 + (2 * exponent)
    return total // 2 + 1

def main():
    primes = list(primerange(1, 100))
    factors = [(primes[i], 0) for i in range(lid)]
    smallest = Integer('9999999999999999')

    for i in range(top):
        factors[0] = (primes[0], i)
        for j in range(i + 1):
            factors[1] = (primes[1], j)
            for k in range(j + 1):
                factors[2] = (primes[2], k)
                for l in range(k + 1):
                    factors[3] = (primes[3], l)
                    for m in range(l + 1):
                        factors[4] = (primes[4], m)
                        for n in range(m + 1):
                            factors[5] = (primes[5], n)
                            for o in range(n + 1):
                                factors[6] = (primes[6], o)
                                for p in range(o + 1):
                                    factors[7] = (primes[7], p)
                                    for q in range(p + 1):
                                        factors[8] = (primes[8], q)
                                        for r in range(q + 1):
                                            factors[9] = (primes[9], r)
                                            for s in range(r + 1):
                                                factors[10] = (primes[10], s)
                                                for t in range(s + 1):
                                                    factors[11] = (primes[11], t)
                                                    if solns(factors) > target and smallest > evaluate(factors):
                                                        smallest = evaluate(factors)

    print(smallest)

if __name__ == "__main__":
    main()
