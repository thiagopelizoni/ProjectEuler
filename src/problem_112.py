# Problem: https://projecteuler.net/problem=112
def is_bouncy(n):
    increasing = decreasing = True
    last_digit = n % 10
    n //= 10
    while n > 0:
        digit = n % 10
        n //= 10
        if digit > last_digit:
            increasing = False
        elif digit < last_digit:
            decreasing = False
        last_digit = digit
        if not increasing and not decreasing:
            return True
    return False

def find_bouncy_number(target_proportion):
    count_bouncy = 0
    number = 99
    while True:
        number += 1
        if is_bouncy(number):
            count_bouncy += 1
        if count_bouncy / number == target_proportion:
            return number

least_number = find_bouncy_number(0.99)
print(least_number)
