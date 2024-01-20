# Problem: https://projecteuler.net/problem=57
def answer(iterations):
    numerator, denominator = 3, 2
    count = 0
    for _ in range(1, iterations):
        numerator, denominator = numerator + 2 * denominator, numerator + denominator
        if len(str(numerator)) > len(str(denominator)):
            count += 1
    return count

print(answer(1000))
