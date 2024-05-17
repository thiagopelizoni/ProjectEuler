# Problem: https://projecteuler.net/problem=117
import numpy as np

def count_ways(length):
    dp = np.zeros(length + 1, dtype=np.int64)
    dp[0] = 1
    for i in range(1, length + 1):
        dp[i] += dp[i - 1]
        if i >= 2:
            dp[i] += dp[i - 2]
        if i >= 3:
            dp[i] += dp[i - 3]
        if i >= 4:
            dp[i] += dp[i - 4]
    return dp[length]

if __name__ == "__main__":
    length = 50
    answer = count_ways(length)
    print(answer)