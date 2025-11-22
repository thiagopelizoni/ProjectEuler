# Problem: https://projecteuler.net/problem=401
from tqdm import tqdm
import math


def sum_of_squares(n, mod):
    if n < 0:
        return 0
    a = n
    b = n + 1
    c = 2 * n + 1
    if a % 2 == 0:
        a //= 2
    else:
        b //= 2
    if a % 3 == 0:
        a //= 3
    elif b % 3 == 0:
        b //= 3
    else:
        c //= 3
    return (a % mod * (b % mod) * (c % mod)) % mod


def main():
    LIMIT = 10**15
    MOD = 10**9
    ans = 0
    i = 1
    approx_iters = int(2 * math.sqrt(LIMIT))
    with tqdm(total=approx_iters) as pbar:
        while i <= LIMIT:
            q = LIMIT // i
            j = LIMIT // q + 1
            cursum = (sum_of_squares(j - 1, MOD) - sum_of_squares(i - 1, MOD) + MOD) % MOD
            ans = (ans + q * cursum % MOD) % MOD
            i = j
            pbar.update(1)
    print(ans)


if __name__ == "__main__":
    main()