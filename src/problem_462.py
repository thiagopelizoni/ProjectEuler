# Problem: https://projecteuler.net/problem=462
from decimal import Decimal, getcontext
from math import floor

def main():
    N = 10**18
    max_a = 0
    while (1 << max_a) <= N:
        max_a += 1

    max_a -= 1
    lambda_part = []
    for a in range(max_a + 1):
        current = 1 << a
        M = N // current
        p = 1
        k = 0
        while p * 3 <= M:
            p *= 3
            k += 1
        lambda_part.append(k + 1)

    n = sum(lambda_part)
    max_col = lambda_part[0]
    conj = []
    for j in range(1, max_col + 1):
        count = 0
        for lam in lambda_part:
            if lam >= j:
                count += 1
            else:
                break
        conj.append(count)

    getcontext().prec = 30
    log10_f = Decimal(0)
    for k in range(2, n + 1):
        log10_f += Decimal(k).log10()

    l = len(lambda_part)
    for row in range(1, l + 1):
        lam_r = lambda_part[row - 1]
        for col in range(1, lam_r + 1):
            hook = lam_r - col + conj[col - 1] - row + 1
            log10_f -= Decimal(hook).log10()

    exp = floor(log10_f)
    frac = log10_f - Decimal(exp)
    mant = Decimal(10) ** frac
    result = f"{mant:.10f}e{exp}"
    print(result)

if __name__ == "__main__":
    main()