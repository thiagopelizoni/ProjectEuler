# Problem: https://projecteuler.net/problem=67

def sieve_of_eratosthenes(limit):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False

    return [i for i in range(2, limit + 1) if sieve[i]]

def compute_totients(limit, primes):
    totients = list(range(limit + 1))
    for p in primes:
        for i in range(p, limit + 1, p):
            totients[i] -= totients[i] // p
    return totients

def is_permutation(a, b):
    return sorted(str(a)) == sorted(str(b))

def find_min_ratio_permutation(limit):
    primes = sieve_of_eratosthenes(limit)
    totients = compute_totients(limit, primes)
    min_ratio = float('inf')
    min_n = 0

    for n in range(2, limit):
        phi_n = totients[n]
        ratio = n / phi_n
        if is_permutation(n, phi_n) and ratio < min_ratio:
            min_n = n
            min_ratio = ratio

    return min_n

if __name__ == "__main__":
    limit = 10**7
    answer = find_min_ratio_permutation(limit)
    print(answer)
