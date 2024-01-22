def sieve_of_eratosthenes(limit):
    prime = [True for _ in range(limit + 1)]
    p = 2
    while p * p <= limit:
        if prime[p]:
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1

    return [p for p in range(2, limit) if prime[p]]

def prime_sum_partitions(target, prime_limit):
    primes = sieve_of_eratosthenes(prime_limit)

    partitions = [0] * (target + 1)
    partitions[0] = 1

    for prime in primes:
        for i in range(prime, target + 1):
            partitions[i] += partitions[i - prime]

    for i in range(len(partitions)):
        if partitions[i] > 5000:
            return i

if __name__ == "__main__":
    target = 10_000
    prime_limit = 10_000
    answer = prime_sum_partitions(target, prime_limit)
    print(answer)
