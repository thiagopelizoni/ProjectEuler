# Problem: https://projecteuler.net/problem=23
LIMIT = 28123

def get_divisors_sum(n):
    """Calculate the sum of proper divisors of n."""
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sum(divisors)

def is_abundant(n):
    """Check if a number is abundant."""
    return get_divisors_sum(n) > n

def main():
    # Generate a list of abundant numbers up to LIMIT
    abundant_numbers = [i for i in range(1, LIMIT + 1) if is_abundant(i)]

    abundant_sums = set()
    limit = len(abundant_numbers)
    for i in range(limit):
        for j in range(i, limit):
            sum_abundant = abundant_numbers[i] + abundant_numbers[j]
            if sum_abundant <= LIMIT:
                abundant_sums.add(sum_abundant)

    # Calculate the sum of all the positive integers which cannot be written as the sum of two abundant numbers
    non_abundant_sum = sum(i for i in range(1, LIMIT + 1) if i not in abundant_sums)
    print(non_abundant_sum)

if __name__ == "__main__":
    main()
