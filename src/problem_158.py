# Problem: https://projecteuler.net/problem=158
from math import comb

def eulerian_one_ascent(length_value):
    return (1 << length_value) - length_value - 1

def count_strings_with_one_ascent(length_value, alphabet_size):
    return comb(alphabet_size, length_value) * eulerian_one_ascent(length_value)

def solve():
    alphabet_size = 26
    best_length = 0
    best_value = 0

    for length_value in range(1, alphabet_size + 1):
        current_value = count_strings_with_one_ascent(length_value, alphabet_size)
        if current_value > best_value:
            best_value = current_value
            best_length = length_value

    print(best_value)


if __name__ == "__main__":
    solve()
