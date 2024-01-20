# Problem: https://projecteuler.net/problem=31

def count_ways(total, coins):
    ways = [0] * (total + 1)
    ways[0] = 1

    for coin in coins:
        for i in range(coin, total + 1):
            ways[i] += ways[i - coin]

    return ways[total]

if __name__ == "__main__":
    total_amount = 200
    coins = [1, 2, 5, 10, 20, 50, 100, 200]

    answer = count_ways(total_amount, coins)
    print(answer)
