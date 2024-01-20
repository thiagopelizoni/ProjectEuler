# Problem: https://projecteuler.net/problem=56
def sum_of_digits(n):
    return sum(int(digit) for digit in str(n))

def max_digit_sum(a_max, b_max):
    max_sum = 0
    for a in range(a_max):
        for b in range(b_max):
            digit_sum = sum_of_digits(a ** b)
            max_sum = max(max_sum, digit_sum)
    return max_sum

answer = max_digit_sum(100, 100)
print(answer)
