# Problem: https://projecteuler.net/problem=487
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import sympy

def compute_for_p(p):
    n = 10**12
    k = 10000

    r = n % p

    B = [0] * (k + 2)
    B[0] = 1
    pascal_row = [1]
    current_n = 0

    fk = 0
    fkp1 = 0

    for m in tqdm(range(1, k + 2)):
        while current_n < m + 1:
            current_n += 1

            new_row = [0] * (current_n + 1)
            new_row[0] = 1
            new_row[current_n] = 1
            for j in range(1, current_n):
                new_row[j] = (pascal_row[j - 1] + pascal_row[j]) % p

            pascal_row = new_row

        sum_s = 0
        for j in range(m):
            if j > 1 and j % 2 == 1:
                continue
            sum_s = (sum_s + pascal_row[j] * B[j]) % p

        inv_m1 = pow(m + 1, p - 2, p)
        B[m] = (-sum_s * inv_m1) % p

        if m == k:
            inv = pow(k + 1, p - 2, p)
            sum_f = 0

            for j in range(k + 1):
                if j > 1 and j % 2 == 1:
                    continue
                sign = 1 if j % 2 == 0 else -1
                term = sign * pascal_row[j] * B[j] % p
                term = term * pow(r, k + 1 - j, p) % p
                sum_f = (sum_f + term) % p

            fk = sum_f * inv % p

    inv = pow(k + 2, p - 2, p)
    sum_f = 0

    for j in range(k + 2):
        if j > 1 and j % 2 == 1:
            continue
        sign = 1 if j % 2 == 0 else -1
        term = sign * pascal_row[j] * B[j] % p
        term = term * pow(r, k + 2 - j, p) % p
        sum_f = (sum_f + term) % p

    fkp1 = sum_f * inv % p

    np1 = (n + 1) % p
    S = (np1 * fk - fkp1) % p

    return S


def main():
    start = 2000000000
    end = 2000002000

    primes = [i for i in range(start, end + 1) if sympy.isprime(i)]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_for_p, primes))

    total = sum(results)

    print(total)


if __name__ == "__main__":
    main()