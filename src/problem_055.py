# Problem: https://projecteuler.net/problem=55
def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]

def reverse_and_add(number):
    """Reverse the digits of a number and add it to the original number."""
    return number + int(str(number)[::-1])

def is_lychrel(number, max_iterations=50):
    """Check if a number is a Lychrel number."""
    for _ in range(max_iterations):
        number = reverse_and_add(number)
        if is_palindrome(str(number)):
            return False
    return True

def count_lychrel_numbers_below_limit(limit):
    """Count the number of Lychrel numbers below a certain limit."""
    count = 0
    for n in range(1, limit):
        if is_lychrel(n):
            count += 1
    return count

if __name__ == "__main__":
    limit = 10000
    answer = count_lychrel_numbers_below_limit(limit)
    print(answer)
