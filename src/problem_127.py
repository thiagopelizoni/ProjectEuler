# Problem: https://projecteuler.net/problem=127
import math
import numpy as np

def main():
    limit = 120000
    radicals = np.array([0] + [1] * (limit - 1))
    for i in range(2, len(radicals)):
        if radicals[i] == 1:
            for j in range(i, len(radicals), i):
                radicals[j] *= i

    sorted_radicals = sorted((rad, n) for (n, rad) in enumerate(radicals))
    sorted_radicals = sorted_radicals[1:]

    result = 0
    for c in range(2, limit):
        for (rad, a) in sorted_radicals:
            rad *= radicals[c]
            if rad >= c:
                break
            b = c - a
            if a < b and rad * radicals[b] < c and math.gcd(a, b) == 1:
                result += c
    return str(result)

if __name__ == "__main__":
    print(main())