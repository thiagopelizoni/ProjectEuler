# Problem: https://projecteuler.net/problem=125
import numpy as np

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def palindromic_sums(limit):
    palindromes = set()
    for i in range(1, int(np.sqrt(limit)) + 1):
        sum_squares = i * i
        for j in range(i + 1, int(np.sqrt(limit)) + 1):
            sum_squares += j * j
            if sum_squares >= limit:
                break
            if is_palindrome(sum_squares):
                palindromes.add(sum_squares)
    return sum(palindromes)

if __name__ == '__main__':
    limit = 10**8
    result = palindromic_sums(limit)
    print(result)
