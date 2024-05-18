# Problem: https://projecteuler.net/problem=114
def main():
    total_length = 50
    ways = [0] * (total_length + 1)
    for length in range(total_length + 1):
        if length < 3:
            ways[length] = 1
        else:
            ways[length] = ways[length - 1] + sum(ways[:length - 3]) + 1
    return str(ways[-1])

if __name__ == "__main__":
    print(main())