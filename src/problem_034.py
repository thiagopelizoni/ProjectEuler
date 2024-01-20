# Problem: https://projecteuler.net/problem=34
from math import factorial

def sum_of_factorials(n):
    return sum(factorial(int(digit)) for digit in str(n))

def find_special_numbers():
    special_numbers = []
    upper_limit = 7 * factorial(9)

    for i in range(10, upper_limit):
        if i == sum_of_factorials(i):
            special_numbers.append(i)
    return special_numbers

if __name__ == "__main__":
    special_numbers = find_special_numbers()
    answer = sum(special_numbers)
    print(answer)
