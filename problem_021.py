# Problem: https://projecteuler.net/problem=21
import math

def sum_of_divisors(n):
    """Returns the sum of proper divisors of n (excluding n itself)."""
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sum(divisors)

def main():
    """ Finding the sum of all the amicable numbers under 10000 """
    amicable_sum = 0

    for a in range(1, 10000):
        b = sum_of_divisors(a)
        if a != b and sum_of_divisors(b) == a:
            amicable_sum += a

    print(amicable_sum)

if __name__ == "__main__":
    main()
