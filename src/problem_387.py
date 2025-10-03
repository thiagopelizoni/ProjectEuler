# Problem: https://projecteuler.net/problem=387
from sympy import isprime
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 387: find the sum of all strong, right-truncatable Harshad primes
    less than 10^14.

    Method / Math Rationale
    ------------------------
    Iteratively generate right-truncatable Harshad numbers by appending digits 0-9 and checking
    if the new number is divisible by the updated sum of digits.

    For each generated Harshad number, check if it is strong by testing if the quotient (number
    divided by digit sum) is prime using sympy.isprime.

    If strong, append each digit 0-9 to form candidate primes, check if they are prime and less
    than 10^14, and add them to the total sum.

    This builds the numbers digit by digit up to 13 digits for Harshad numbers, ensuring all
    right-truncatable properties are maintained.

    Complexity
    ----------
    Time: O((max_digits - 1) * H * 10 * log(N)), where max_digits=14, H is the max number of
    Harshad numbers at a level (small, ~10^4), and log(N) is the cost of isprime for N<10^14.

    Space: O(H) for storing current Harshad numbers.

    References
    ----------
    https://projecteuler.net/problem=387
    """
    limit = 10**14
    total = 0
    current_harshads = [(d, d) for d in range(1, 10)]
    for _ in tqdm(range(13)):
        new_harshads = []
        for num, s in current_harshads:
            quotient = num // s
            if isprime(quotient):
                for d in range(10):
                    candidate = num * 10 + d
                    if candidate < limit and isprime(candidate):
                        total += candidate
            for d in range(10):
                new_num = num * 10 + d
                new_s = s + d
                if new_s != 0 and new_num % new_s == 0:
                    new_harshads.append((new_num, new_s))
        current_harshads = new_harshads
    print(total)

if __name__ == "__main__":
    main()