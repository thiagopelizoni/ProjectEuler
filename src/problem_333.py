# Problem: https://projecteuler.net/problem=333
import numpy as np
from tqdm import tqdm
from sympy.ntheory import isprime

def main():
    """
    Purpose
    ------
    Solves Project Euler problem 333 by computing the sum of primes q < 1000000 such that P(q) = 1,
    where P(q) is the number of special partitions.

    Method / Math Rationale
    -----------------------
    Uses dynamic programming to count the number of valid antichains summing to each number up to the limit.
    The DP state tracks the current sum and the last used power of 3 (b), adding terms with increasing powers of 2 (a)
    and decreasing b to ensure the antichain property (no term divides another). Single and multi-term partitions are
    handled naturally. Ways are capped at 2 since we only need to know if P(n) == 1.

    Complexity
    ----------
    O(max_a * limit * max_b) ~ 3.6e8 operations.

    References
    ----------
    https://projecteuler.net/problem=333
    """
    limit = 999999
    max_a = 0
    while (1 << max_a) <= limit:
        max_a += 1
    max_a -= 1
    max_b = 0
    three = 1
    while three <= limit:
        max_b += 1
        three *= 3
    max_b -= 1
    inf_b = max_b + 1
    last_b_dim = inf_b + 1
    vals = np.zeros((max_a + 1, max_b + 1), dtype=int)
    for a in range(max_a + 1):
        p2 = 1 << a
        for b in range(max_b + 1):
            vals[a][b] = p2 * (3 ** b)
    dp = np.zeros((2, limit + 1, last_b_dim), dtype=np.uint8)
    curr = 0
    dp[curr][0][inf_b] = 1
    for a in range(max_a + 1):
        next_ = 1 - curr
        dp[next_] = 0
        for s in tqdm(range(limit + 1)):
            for lb in range(last_b_dim):
                ways = dp[curr][s][lb]
                if ways == 0:
                    continue
                dp[next_][s][lb] += ways
                max_bb = lb - 1
                for b in range(max_bb + 1):
                    v = vals[a][b]
                    new_s = s + v
                    if new_s > limit:
                        continue
                    dp[next_][new_s][b] += ways
        dp[next_] = np.minimum(dp[next_], 2)
        curr = next_
    total_sum = 0
    for i in range(2, limit + 1):
        num_ways = np.sum(dp[curr][i])
        if num_ways == 1 and isprime(i):
            total_sum += i
    print(total_sum)

if __name__ == "__main__":
    main()