# Problem: https://projecteuler.net/problem=267
import math
from decimal import Decimal, getcontext
from tqdm import tqdm


def euler267_probability(n: int = 1000,
                         target: int = 10**9,
                         precision: int = 50,
                         use_tqdm: bool = True) -> Decimal:
    """
    Compute the probability posed in Project Euler 267 that an
    optimal fixed-fraction betting strategy reaches at least a
    target bankroll after n independent flips. Each flip multiplies
    the bankroll by 2 with probability p (heads) and by 1/2 with
    probability 1 - p (tails). The routine finds the smallest
    integer w such that the large-deviation threshold is met, then
    evaluates the complementary binomial tail via an exact-sum of
    combinations in high precision.

    Args:
        n: Number of flips.
        target: Bankroll threshold to reach or exceed.
        precision: Decimal precision used for intermediate arithmetic.
        use_tqdm: Whether to show a progress bar during the binomial sum.

    Returns:
        Decimal: The probability that the optimal fixed-fraction strategy
        attains at least the target bankroll after n flips.
    """
    getcontext().prec = precision

    ln_target = math.log(target)
    thresh = ln_target / n

    w = int(n / 3) + 1
    while True:
        p = w / n
        if p * math.log(2 * p) + (1 - p) * math.log(1 - p) + math.log(3 / 2) >= thresh:
            break
        w += 1

    m = w - 1

    sum_comb = Decimal(1)
    current_comb = Decimal(1)

    iterator = tqdm(range(1, m + 1)) if use_tqdm else range(1, m + 1)
    for k in iterator:
        current_comb = current_comb * Decimal(n - k + 1) / Decimal(k)
        sum_comb += current_comb

    total = Decimal(2) ** n
    prob_small = sum_comb / total
    prob = Decimal(1) - prob_small

    return prob


if __name__ == "__main__":
    getcontext().prec = 50
    prob = euler267_probability()
    print(format(float(prob), '.12f'))
