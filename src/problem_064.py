# Problem: https://projecteuler.net/problem=64
import math

def continued_fraction_sqrt(n):
    m = 0
    d = 1
    a0 = int(math.sqrt(n))
    an = a0
    period = 0

    if a0 != math.sqrt(n):
        while an != 2 * a0:
            m = d * an - m
            d = (n - m * m) // d
            an = (a0 + m) // d
            period += 1

    return period

if __name__ == "__main__":
    answer = sum(continued_fraction_sqrt(i) % 2 != 0 for i in range(2, 10001))
    print(answer)
