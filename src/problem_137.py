# Problem: https://projecteuler.net/problem=137
from math import isqrt

def main():
    target = 12
    count = 0
    answer = 0

    n = 1
    while count < target:
        MC_candidates = []

        if (sqrt := isqrt(5 * n * n + 1)) ** 2 == 5 * n * n + 1:
            MC_candidates.append(2 * n + sqrt)
        if (sqrt := isqrt(5 * n * n - 1)) ** 2 == 5 * n * n - 1:
            MC_candidates.append(2 * n + sqrt)
        if (sqrt := isqrt(5 * n * n + 2)) ** 2 == 5 * n * n + 2:
            MC_candidates.append(n + sqrt)
        if (sqrt := isqrt(5 * n * n - 2)) ** 2 == 5 * n * n - 2:
            MC_candidates.append(n + sqrt)

        for m in MC_candidates:
            a, b, c = m * m - n * n, 2 * m * n, m * m + n * n
            count += 1
            answer += c
            print(a, b, c)

        n += 1

    print(f"Answewr: {answer}")


if __name__ == "__main__":
    main()
