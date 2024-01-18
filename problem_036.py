# Problem: https://projecteuler.net/problem=36
def is_palindrome(s):
    return s == s[::-1]

def double_base_palindromes(limit):
    total_sum = 0
    for i in range(1, limit):
        if is_palindrome(str(i)) and is_palindrome(format(i, 'b')):
            total_sum += i
    return total_sum

limit = 1000000
answer = double_base_palindromes(limit)
print(answer)
