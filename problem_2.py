# Problem: https://projecteuler.net/problem=2

LIMIT = 4000000

def sum_fibonacci_pairs(limit):
    result = 0
    a, b = 1, 2
    while a <= limit:
        if a % 2 == 0:
            result += a
        a, b = b, a + b
    return result

if __name__ == "__main__":
    answer = sum_fibonacci_pairs(LIMIT)
    print(answer)
