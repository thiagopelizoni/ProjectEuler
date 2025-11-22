# Problem: https://projecteuler.net/problem=293
from sympy.ntheory.generate import nextprime
from tqdm import tqdm

def generate_admissible(primes, limit):
    result = set()

    def rec(index, current):
        if index == len(primes):
            result.add(current)
            return
        p = primes[index]
        val = current * p
        while val < limit:
            rec(index + 1, val)
            val *= p

    rec(0, 1)
    return result

def main():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    limit = 10**9
    all_n = set()
    for k in range(1, 10):
        current_primes = primes[:k]
        all_n.update(generate_admissible(current_primes, limit))
    pseudo_fortunate = set()
    for n in tqdm(sorted(all_n)):
        m = nextprime(n + 1) - n
        pseudo_fortunate.add(m)
    print(sum(pseudo_fortunate))

if __name__ == "__main__":
    main()