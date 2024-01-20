# Problem: https://projecteuler.net/problem=50
def sieve_of_eratosthenes(limit):
    primes = []
    sieve = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
    return primes

def longest_sum_of_consecutive_primes(limit):
    # Find the prime below one-million which can be written as the sum of the most consecutive primes
    primes = sieve_of_eratosthenes(limit)
    max_length = 0
    max_prime = 0
    total_primes = len(primes)

    for i in range(total_primes):
        for j in range(i + max_length, total_primes):
            sum_primes = sum(primes[i:j])
            if sum_primes < limit:
                if sum_primes in primes:
                    max_length = j - i
                    max_prime = sum_primes
            else:
                break

    return max_prime

answer = longest_sum_of_consecutive_primes(1000000)
print(answer)
