# Problem: https://projecteuler.net/problem=318
from decimal import Decimal, getcontext, ROUND_CEILING
from math import floor
from tqdm import tqdm

def main():
    getcontext().prec = 100
    total = 0
    max_sum = 2011
    one = Decimal(1)
    two = Decimal(2)
    eps = Decimal('1e-50')
    target = Decimal(2011)
    for p in tqdm(range(1, max_sum // 2 + 2)):
        sqrt_p = Decimal(p).sqrt()
        max_q_dec = (sqrt_p + one) ** 2 - eps
        max_q = min(max_sum - p, floor(max_q_dec))
        for q in range(p + 1, max_q + 1):
            sqrt_q = Decimal(q).sqrt()
            diff = sqrt_q - sqrt_p
            if diff >= one:
                continue
            r = Decimal(q - p)
            arg = (sqrt_q + sqrt_p) / r
            lambda_val = two * arg.log10()
            div = target / lambda_val
            n_dec = div.to_integral_value(rounding=ROUND_CEILING)
            total += int(n_dec)
    print(total)

if __name__ == "__main__":
    main()