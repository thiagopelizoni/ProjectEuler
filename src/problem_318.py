# Problem: https://projecteuler.net/problem=318
from decimal import Decimal, getcontext, ROUND_CEILING
from math import floor
from tqdm import tqdm

def main():
    """
    Purpose
    Solve Project Euler problem 318: find the sum of the minimal n such that the number of leading 9s in the
    fractional part of (√p + √q)^{2n} is at least 2011, over all qualifying p < q with p + q ≤ 2011.

    Method / Math Rationale
    For each valid pair (p, q), compute δ = (√q - √p)^2 < 1. The number of leading 9s is floor(n * λ) where
    λ = -log10(δ). The minimal n is the smallest integer such that n λ ≥ 2011, i.e., ceil(2011 / λ). λ is
    computed as 2 * log10((√q + √p) / (q - p)). Sum these n.

    Complexity
    O(S * log P) time where S ≈ 2011/2 * √2011 ≈ 30,000 is the number of pairs, P=2011; negligible.

    References
    https://projecteuler.net/problem=318
    """
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