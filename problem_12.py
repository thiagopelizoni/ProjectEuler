# Problem: https://projecteuler.net/problem=12

def count_divisors(n):
    divisors = 0
    sqrt_n = int(n**0.5)
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            divisors += 2
    if sqrt_n * sqrt_n == n:
        divisors -= 1
    return divisors

def find_triangular(min_divisors):
    num = 1
    triangle = 0

    while True:
        triangle += num
        if count_divisors(triangle) > min_divisors:
            return triangle
        num += 1

if __name__ == "__main__":
    answer = find_triangular(500)
    print(answer)
