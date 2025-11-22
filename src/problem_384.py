# Problem: https://projecteuler.net/problem=384
from functools import lru_cache
from tqdm import tqdm

@lru_cache(maxsize=None)
def r(n):
    if n == 0:
        return 1

    if n % 2 == 0:
        return r(n // 2)
    else:
        return ((-1) ** (n // 2)) * r(n // 2)


@lru_cache(maxsize=None)
def s(n):
    if n < 0:
        return 0

    if n == 0:
        return 1

    q = n // 4
    rem = n % 4
    s_q = s(q)
    r_q = r(q)

    if rem == 0:
        return 2 * s_q - r_q
    elif rem == 1:
        return 2 * s_q
    elif rem == 2:
        return 2 * s_q + ((-1) ** q) * r_q
    else:
        return 2 * s_q


@lru_cache(maxsize=None)
def count_to(n: int, t: int, par=None, r_sign=None) -> int:
    if n < 0:
        return 0

    if n == 0:
        if s(0) != t:
            return 0
        if par is not None and par != 0:
            return 0
        if r_sign is not None and r_sign != 1:
            return 0
        return 1

    q = n // 4
    rem = n % 4

    if rem == 3:
        total = 0
        for j in range(4):
            k_par = j % 2
            if par is not None and par != k_par:
                continue
            for p_k in [0, 1]:
                minus_one_k = 1 if p_k == 0 else -1
                for r_k in [1, -1]:
                    offs = 0
                    if j == 0:
                        offs = -r_k
                    elif j == 1:
                        offs = 0
                    elif j == 2:
                        offs = minus_one_k * r_k
                    elif j == 3:
                        offs = 0
                    if (t - offs) % 2 != 0:
                        continue
                    v = (t - offs) // 2
                    k_r = 0
                    if j == 0 or j == 1:
                        k_r = r_k
                    elif j == 2:
                        k_r = minus_one_k * r_k
                    elif j == 3:
                        k_r = -minus_one_k * r_k
                    if r_sign is not None and r_sign != k_r:
                        continue
                    total += count_to(q, v, p_k, r_k)
        return total
    else:
        sub_n = 4 * q - 1
        total = count_to(sub_n, t, par, r_sign)
        for j in range(rem + 1):
            k = 4 * q + j
            if s(k) == t:
                k_par = j % 2
                k_r = r(k)
                if par is None or par == k_par:
                    if r_sign is None or r_sign == k_r:
                        total += 1
        return total


def find_g(t_val, c):
    low = 0
    high = 10**19

    while low < high:
        mid = (low + high) // 2
        if count_to(mid, t_val) >= c:
            high = mid
        else:
            low = mid + 1

    return low


def main():
    F = [0] * 46
    F[0] = 1
    F[1] = 1

    for i in range(2, 46):
        F[i] = F[i - 1] + F[i - 2]

    total = 0
    for t in tqdm(range(2, 46)):
        t_val = F[t]
        c = F[t - 1]
        g = find_g(t_val, c)
        total += g

    print(total)


if __name__ == "__main__":
    main()