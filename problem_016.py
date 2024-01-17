# Problem: https://projecteuler.net/problem=15

def sum_of_digits(base, power):
    """
    Function to calculate the sum of the digits of the number base raised to the power.
    """
    number = base ** power
    return sum(map(int, str(number)))

# Calculate the sum of the digits of the number 2^1000
if __name__ == "__main__":
    answer = sum_of_digits(2, 1000)
    print(answer)
