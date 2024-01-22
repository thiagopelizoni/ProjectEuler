# Problem: https://projecteuler.net/problem=78
def pentagonal_number(k):
    return k * (3 * k - 1) // 2

def generalized_pentagonal_number(n):
    if n % 2 == 0:
        return pentagonal_number(n // 2 + 1)
    else:
        return pentagonal_number(-(n // 2 + 1))

def partition_function_divisible_by(million, limit):
    partitions = [0] * (limit + 1)
    partitions[0] = 1

    for n in range(1, limit + 1):
        i = 0
        k = 1
        while k <= n:
            sign = -1 if (i % 4 > 1) else 1
            partitions[n] += sign * partitions[n - k]
            partitions[n] %= million
            i += 1
            k = generalized_pentagonal_number(i)

        if partitions[n] == 0:
            return n
    return -1

if __name__ == "__main__":
    limit = 100_000

    # Divisibility target
    million = 1_000_000
    answer = partition_function_divisible_by(million, limit)
    print(answer)
