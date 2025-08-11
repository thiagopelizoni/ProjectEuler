# Problem: https://projecteuler.net/problem=143
from math import isqrt
from gmpy2 import gcd


def generate_pairs(limit_sum):
    pair_exists = set()
    neighbor_map = {}

    max_m = int((limit_sum * 3) ** 0.5) + 2

    for m in range(2, max_m):
        m_squared = m * m

        for n in range(1, m):
            if gcd(m, n) != 1:
                continue

            if (m - n) % 3 == 0:
                continue

            n_squared = n * n
            u0 = m_squared - n_squared
            v0 = 2 * m * n + n_squared

            if u0 <= 0:
                continue

            if u0 > limit_sum and v0 > limit_sum:
                break

            max_k = min(limit_sum // u0, limit_sum // v0)

            for k in range(1, max_k + 1):
                u = k * u0
                v = k * v0

                if u <= limit_sum and v <= limit_sum:
                    a = u
                    b = v

                    if a not in neighbor_map:
                        neighbor_map[a] = []
                    if b not in neighbor_map:
                        neighbor_map[b] = []

                    neighbor_map[a].append(b)
                    neighbor_map[b].append(a)

                    if a < b:
                        pair_exists.add((a, b))
                    else:
                        pair_exists.add((b, a))

    return neighbor_map, pair_exists


def find_distinct_sums(limit_sum, neighbor_map, pair_exists):
    distinct_sums = set()

    for shared_leg, neighbors in neighbor_map.items():
        sorted_neighbors = sorted(neighbors)

        for i in range(len(sorted_neighbors)):
            first_leg = sorted_neighbors[i]

            if shared_leg + first_leg >= limit_sum:
                break

            for j in range(i + 1, len(sorted_neighbors)):
                second_leg = sorted_neighbors[j]
                total_length = shared_leg + first_leg + second_leg

                if total_length > limit_sum:
                    break

                key_pair = (first_leg, second_leg) if first_leg < second_leg else (second_leg, first_leg)

                if key_pair in pair_exists:
                    distinct_sums.add(total_length)

    return sum(distinct_sums)


def main():
    limit_sum = 120000
    neighbor_map, pair_exists = generate_pairs(limit_sum)
    result = find_distinct_sums(limit_sum, neighbor_map, pair_exists)
    print(result)


if __name__ == "__main__":
    main()
