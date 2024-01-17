# Problem: https://projecteuler.net/problem=5
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def smallest_multiple(n):
    lcm_result = 1
    for i in range(1, n + 1):
        lcm_result = lcm(lcm_result, i)
    return lcm_result

if __name__ == "__main__":
    n = 20
    answer = smallest_multiple(n)
    print(answer)
