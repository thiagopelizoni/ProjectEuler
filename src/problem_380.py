# Problem: https://projecteuler.net/problem=380
from tqdm import tqdm
import math

def main():
    m = 100
    n = 500
    sum_log10 = 0.0
    for p in tqdm(range(1, m + 1)):
        arg_p = math.pi * (p - 1) / m
        lp = 2 - 2 * math.cos(arg_p)
        for q in range(1, n + 1):
            arg_q = math.pi * (q - 1) / n
            lq = 2 - 2 * math.cos(arg_q)
            term = lp + lq
            if term > 0:
                sum_log10 += math.log10(term)

    sum_log10 -= math.log10(m * n)
    exponent = math.floor(sum_log10)
    frac = sum_log10 - exponent
    mant = 10 ** frac
    rounded_mant = round(mant, 4)

    if rounded_mant >= 10:
        rounded_mant /= 10
        exponent += 1

    print(f"{rounded_mant:.4f}e{exponent}")

if __name__ == "__main__":
    main()