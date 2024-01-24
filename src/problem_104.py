# Problem: https://projecteuler.net/problem=104
import math

# Constants for modulo operations
MOD = 10**9

# Fast doubling method to compute Fibonacci numbers modulo 10**9
def fibonacci_mod(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = fibonacci_mod(n >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if n & 1:
            return (d % MOD, (c + d) % MOD)
        else:
            return (c % MOD, d % MOD)

# Check if a number is 1 to 9 pandigital
def is_pandigital(n):
    digits = str(n)
    return len(digits) == 9 and set(digits) == set('123456789')

# Find the index k of the Fibonacci number where both first and last 9 digits are pandigital
def pandigital_fibonacci():
    k, a, b = 2, 1, 1
    while True:
        # Check last nine digits for pandigital
        if is_pandigital(b):
            # Compute first nine digits using log
            phi = (1 + math.sqrt(5)) / 2
            log_fib_k = k * math.log10(phi) - 0.5 * math.log10(5)
            first_nine_digits = int(pow(10, log_fib_k - int(log_fib_k) + 8))

            # Check first nine digits for pandigital
            if is_pandigital(first_nine_digits):
                return k

        k += 1
        a, b = b, (a + b) % MOD

pandigital_index = pandigital_fibonacci()
print(pandigital_index)
