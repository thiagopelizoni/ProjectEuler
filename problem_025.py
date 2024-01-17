# Problem: https://projecteuler.net/problem=25

def find_fibonacci_index(digit_count):
    a, b = 1, 1
    index = 2

    while True:
        a, b = b, a + b
        index += 1

        if len(str(b)) >= digit_count:
            return index

def main():
    """ Find the index of the first Fibonacci number to have 1000 digits """
    index_1000_digits = find_fibonacci_index(1000)
    print(index_1000_digits)

if __name__ == "__main__":
    main()
