# Problem: https://projecteuler.net/problem=251
import math
from tqdm import tqdm
from numba import njit

LIMIT_N = 110_000_000

@njit
def extended_gcd(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


@njit
def mod_inverse_numba(a, m):
    g, x, y = extended_gcd(a, m)
    return (x % m + m) % m


@njit
def solve_y_layer(y, limit_n):
    count = 0
    m_mod = 8 * y
    x = 1
    while True:
        a_g, b_g = x, y
        while b_g:
            a_g, b_g = b_g, a_g % b_g

        if a_g != 1:
            x += 2
            continue

        x2 = x * x
        term1 = x2 * x
        term2 = 3 * x2 * y
        term3 = 8 * y * y * y
        denom = term1 + term2 + term3
        num = 8 * y * limit_n - y - 3 * x

        if num < denom:
            break

        k_max = num // denom
        inv_x2 = mod_inverse_numba(x2, m_mod)
        k0 = (inv_x2 * (m_mod - 3)) % m_mod

        if k0 == 0:
            k0 = m_mod

        if k0 <= k_max:
            count += (k_max - k0) // m_mod + 1

        x += 2

    return count


def solve_chunk(y_range):
    local_count = 0
    for y in y_range:
        m_mod = 8 * y
        x = 1
        limit_n = LIMIT_N

        while True:
            if math.gcd(x, y) != 1:
                x += 2
                continue

            x2 = x * x
            x3 = x2 * x
            denom = x3 + 3 * x2 * y + 8 * y * y * y
            num = 8 * y * limit_n - y - 3 * x

            if num < denom:
                break

            k_max = num // denom
            inv_x2 = pow(x2, -1, m_mod)
            k0 = (inv_x2 * (m_mod - 3)) % m_mod
            if k0 == 0:
                k0 = m_mod

            if k0 <= k_max:
                local_count += (k_max - k0) // m_mod + 1

            x += 2
    return local_count


def main():
    limit_n = LIMIT_N
    y_limit = int(limit_n**0.5) + 100
    y_values = range(1, y_limit)
    total_triplets = 0

    for y in tqdm(y_values, desc="Calculando (Numba)", unit="y"):
        total_triplets += solve_y_layer(y, limit_n)

    print(total_triplets)


if __name__ == "__main__":
    main()