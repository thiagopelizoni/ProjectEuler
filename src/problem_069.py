# Problem: https://projecteuler.net/problem=69
def sieve(limit):
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit, i):
                sieve[j] = False
    return [i for i in range(2, limit) if sieve[i]]

def find_max_n_phi_ratio(limit):
    primes = sieve(int(limit**0.5) + 1)
    n = 1
    for p in primes:
        if n * p > limit:
            break
        n *= p
    return n

if __name__ == "__main__":
    limit = 1_000_000
    answer = find_max_n_phi_ratio(limit)
    print(answer)
