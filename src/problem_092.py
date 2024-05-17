# Problem: https://projecteuler.net/problem=92
def next_number(n):
    return sum(int(digit) ** 2 for digit in str(n))

def arrives_at_89(n):
    while n != 1 and n != 89:
        n = next_number(n)
    return n == 89

count = sum(arrives_at_89(n) for n in range(1, 10000000))
print(count)
