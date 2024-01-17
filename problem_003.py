# Problem: https://projecteuler.net/problem=3

LPF = 600851475143

def largest_prime_factor(n):
    factor = 2
    while factor * factor <= n:
        if n % factor:
            factor += 1
        else:
            n //= factor
    return n

if __name__ == "__main__":
    result = largest_prime_factor(LPF)
    print(result)
