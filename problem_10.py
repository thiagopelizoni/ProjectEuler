# Problem: https://projecteuler.net/problem=10

N = 2000000

def sum_of_primes_below(n):
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n, i):
                sieve[j] = False
    return sum(i for i in range(n) if sieve[i])

if __name__ == "__main__":
    answer = sum_of_primes_below(N)
    print(answer)
