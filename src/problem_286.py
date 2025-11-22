# Problem: https://projecteuler.net/problem=286
from decimal import Decimal, getcontext
from tqdm import tqdm

def compute_prob(q: Decimal) -> Decimal:
    dp = [Decimal(0)] * 51
    dp[0] = Decimal(1)
    for x in range(1, 51):
        p_score = Decimal(1) - Decimal(x) / q
        p_not = Decimal(1) - p_score
        new_dp = [Decimal(0)] * 51
        for j in range(51):
            new_dp[j] += dp[j] * p_not
            if j < 50:
                new_dp[j + 1] += dp[j] * p_score
        dp = new_dp
    return dp[20]

def main():
    getcontext().prec = 60
    low = Decimal('50.0000000000000000000000000000000000000000000000000000000001')
    high = Decimal('1000')
    target = Decimal('0.02')
    iterations = 200
    for _ in tqdm(range(iterations)):
        mid = (low + high) / Decimal(2)
        prob = compute_prob(mid)
        if prob > target:
            low = mid
        else:
            high = mid
    mid = (low + high) / Decimal(2)
    rounded = mid.quantize(Decimal('0.0000000001'))
    print(rounded)

if __name__ == "__main__":
    main()