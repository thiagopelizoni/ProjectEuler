# Problem: https://projecteuler.net/problem=115
def count_ways(m, length, memo):
    if length in memo:
        return memo[length]
    if length < m:
        return 1
    total_ways = 1
    for start in range(length - m + 1):
        for red_length in range(m, length - start + 1):
            total_ways += count_ways(m, length - start - red_length - 1, memo)
    memo[length] = total_ways
    return total_ways

def min_length_for_blocks(m, n):
    length = m
    memo = {}
    while count_ways(m, length, memo) <= n:
        length += 1
    return length

if __name__ == "__main__":
    m = 50
    n = 1000000
    result = min_length_for_blocks(m, n)
    print(result)