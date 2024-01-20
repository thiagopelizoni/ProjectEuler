# Problem: https://projecteuler.net/problem=14

def collatz_sequence_length(n):
    length = 1
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        length += 1
    return length

def main():
    max_length = 0
    starting_number = 0

    for i in range(1, 1000000):
        length = collatz_sequence_length(i)
        if length > max_length:
            max_length = length
            starting_number = i

    print(starting_number)

if __name__ == "__main__":
    main()
