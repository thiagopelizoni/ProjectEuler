# Problem: https://projecteuler.net/problem=136
import numpy as np

def main():
    limit = 50_000_000
    at_least_one = np.zeros(limit, dtype=bool)
    more_than_one = np.zeros(limit, dtype=bool)

    for a in range(1, limit):
        for b in range((a + 3) // 4, a):
            current = a * (4 * b - a)
            if current >= limit:
                break

            if at_least_one[current]:
                more_than_one[current] = True
            else:
                at_least_one[current] = True

    count = np.sum(at_least_one & ~more_than_one)

    return count

if __name__ == "__main__":
    print(main())