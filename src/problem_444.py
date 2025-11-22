# Problem: https://projecteuler.net/problem=444
from decimal import Decimal, getcontext
from math import factorial

getcontext().prec = 50

def main():
    N = 10**14
    m = 20
    n = Decimal(N + m)
    binom_val = Decimal(1)
    for i in range(1, m + 1):
        binom_val *= (n - Decimal(i - 1)) / Decimal(i)

    gamma = Decimal('0.57721566490153286060651209008240243104215933593992')
    ln_n = n.ln()
    one_over_2n = Decimal(1) / (Decimal(2) * n)
    one_over_12n2 = Decimal(1) / (Decimal(12) * n * n)
    H_large = ln_n + gamma + one_over_2n - one_over_12n2
    H_m = Decimal(0)
    for k in range(1, m + 1):
        H_m += Decimal(1) / Decimal(k)

    diff = H_large - H_m
    result = binom_val * diff
    s = f'{result:.9e}'
    print(s.replace('e+', 'e'))

if __name__ == "__main__":
    main()