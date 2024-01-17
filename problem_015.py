# Problem: https://projecteuler.net/problem=15
from math import factorial

def lattice_paths(n):
    """
    Function to calculate the number of lattice paths in a grid of size n x n
    using the binomial coefficient approach.
    """
    return factorial(2 * n) // (factorial(n) ** 2)

# Calculate the number of lattice paths for a 20x20 grid
if __name__ == "__main__":
    answer = lattice_paths(20)
    print(answer)
