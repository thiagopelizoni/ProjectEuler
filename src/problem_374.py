import math
from tqdm import tqdm


def find_max_m(N):
    lo = 0
    hi = 10**8

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * (mid + 1) // 2 <= N:
            lo = mid
        else:
            hi = mid - 1

    return lo


def main():
    N = 10**14
    P = 982451653

    max_m = find_max_m(N)
    M = max_m + 2

    fact = [0] * (M + 1)
    fact[0] = 1

    for i in range(1, M + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [0] * (M + 1)
    invfact[M] = pow(fact[M], P - 2, P)

    for i in tqdm(range(M, 0, -1)):
        invfact[i - 1] = invfact[i] * i % P

    inv = [0] * (M + 1)
    for i in range(1, M + 1):
        inv[i] = invfact[i] * fact[i - 1] % P

    harm = [0] * (M + 1)
    for i in range(1, M + 1):
        harm[i] = (harm[i - 1] + inv[i]) % P

    total = 0

    if N >= 1:
        total = (total + 1) % P

    for m in range(1, max_m + 1):
        t_m = m * (m + 1) // 2
        l_max = min(m, N - t_m)

        if l_max < 0:
            continue

        sum1 = 0
        if m >= 2:
            if l_max >= m - 2:
                h = (harm[m] - 1 + P) % P
                temp = (m - 1) * fact[m + 1] % P
                sum1 = temp * h % P
            else:
                for l in range(l_max + 1):
                    k = m - l
                    f = fact[m + 1] * inv[k] % P
                    sum1 = (sum1 + f * (m - 1)) % P

        contrib2 = 0
        if m >= 2 and l_max >= m - 1:
            f2 = (m + 2) * fact[m] % P * inv[2] % P
            contrib2 = f2 * (m - 1) % P

        contrib3 = 0
        if l_max >= m:
            f3 = fact[m + 1]
            contrib3 = f3 * m % P

        total = (total + sum1 + contrib2 + contrib3) % P

    print(total)


if __name__ == "__main__":
    main()