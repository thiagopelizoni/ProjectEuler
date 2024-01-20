# Problem: https://projecteuler.net/problem=48
def answer(last_term, last_digits):
    total = sum(i**i for i in range(1, last_term + 1))
    return int(str(total)[-last_digits:])

# Calculate the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000
print(answer(1000, 10))
