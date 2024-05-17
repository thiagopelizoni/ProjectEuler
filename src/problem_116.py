# Problem: https://projecteuler.net/problem=116
import numpy as np

def count_ways(length, tile_length):
    dp = np.zeros(length + 1, dtype=np.int64)
    dp[0] = 1
    for i in range(1, length + 1):
        dp[i] += dp[i - 1]
        if i >= tile_length:
            dp[i] += dp[i - tile_length]
    return dp[length]

if __name__ == "__main__":
    length = 50
    answer = sum(count_ways(length, tile_length) - 1 for tile_length in [2, 3, 4])
    print(answer)