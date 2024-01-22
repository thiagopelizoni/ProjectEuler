# Problem: https://projecteuler.net/problem=76
def partition_function(n):
    partitions = [0] * (n + 1)

    partitions[0] = 1

    limit = n + 1
    for i in range(1, limit):
        for j in range(i, limit):
            partitions[j] += partitions[j - i]

    return partitions[n] - 1

if __name__ == "__main__":
    print(partition_function(100))
