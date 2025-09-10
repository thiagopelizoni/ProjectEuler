# Problem: https://projecteuler.net/problem=301
from tqdm import tqdm

def main():
    """
    Purpose
    Solve Project Euler problem 301 by counting the number of positive integers n <= 2**30 such that n XOR (2*n) XOR (3*n) == 0.

    Method / Math Rationale
    The condition n XOR (2*n) XOR (3*n) == 0 holds if and only if the binary representation of n has no two consecutive 1-bits.
    The number of such positive integers n <= 2**30 is the 32nd Fibonacci number, where the Fibonacci sequence is defined as
    F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, and so on. This is computed using an iterative loop for efficiency.

    Complexity
    O(1) time and space, as the loop runs a fixed number of iterations independent of input size.

    References
    https://projecteuler.net/problem=301
    """
    a = 1
    b = 1
    for _ in tqdm(range(3, 33)):
        a, b = b, a + b
    print(b)

if __name__ == "__main__":
    main()