# Problem: https://projecteuler.net/problem=503
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Computes the minimal expected score F(n) for n=10^6 in the game described in Project Euler problem 503.

    Method / Math Rationale
    ----------------------
    Uses dynamic programming to compute the minimal expected score by considering optimal thresholds
    for accepting a card based on its order statistic in the remaining set. The DP array f[i] represents
    the minimal expected score with i cards remaining. For each i, it tries different thresholds k and
    chooses the one that minimizes the expectation, using order statistics for expected values.

    Complexity
    ----------
    O(n log n) time due to the inner loop being bounded by a decreasing 'up' value, and O(n) space.

    References
    ----------
    https://projecteuler.net/problem=503
    """
    n = 1000000
    f = [0.0] * (n + 1)
    f[n] = (n + 1.0) / 2
    up = n - 1
    for i in tqdm(range(n - 1, 0, -1)):
        f[i] = f[i + 1]
        prob = 1.0
        expe = 0.0
        for k in range(1, up + 1):
            expe += 1.0 / i * (n + 1) / (i + 1) * k
            if expe >= f[i]:
                break
            prob -= 1.0 / i
            if expe + prob * f[i + 1] < f[i]:
                f[i] = expe + prob * f[i + 1]
                up = k
    print(f"{f[1]:.10f}")

if __name__ == "__main__":
    main()