# Problem: https://projecteuler.net/problem=313
from sympy.ntheory import primerange

def main():
    """
    Purpose
    Solve Project Euler problem 313: Count the number of m by n grids such that the minimum number of moves S(m,n) in the sliding game equals p^2,
    where p < 10^6 is a prime number.

    Method / Math Rationale
    Generate all primes p < 10^6 using primerange. For each prime p, add to the total the number of grids: 2 if p == 3, else (p**2 - 1) // 12.
    This formula is derived from the pattern in the values of S(m,n), which allows efficient counting without computing S for each possible grid.

    Complexity
    O(pi(10^6)) time, where pi is the prime-counting function, approximately 10^6 / log(10^6) ≈ 7.8e4 iterations.

    References
    https://projecteuler.net/problem=313
    """
    limit = 1000000
    total = 0
    for p in primerange(2, limit):
        if p == 3:
            total += 2
        else:
            total += (p * p - 1) // 12
    print(total)

if __name__ == "__main__":
    main()