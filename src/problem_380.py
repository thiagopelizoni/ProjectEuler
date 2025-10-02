# Problem: https://projecteuler.net/problem=380
from tqdm import tqdm
import math

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 380: compute the number of distinct 100 x 500 mazes, which is the number
    of spanning trees in a 100 x 500 grid graph, and print it in scientific notation rounded to 5
    significant digits.

    Method / Math Rationale
    ------------------------
    Uses the Matrix-Tree Theorem for the grid graph, which is the Cartesian product of two path graphs.
    The number of spanning trees is (1 / (m * n)) times the product of the nonzero eigenvalues of the
    Laplacian matrix. The eigenvalues are λ_p + μ_q where λ_p = 2 - 2 * cos(π * (p-1) / m) for p = 1
    to m, and similarly for μ_q. Compute the product using sum of log10 to handle large numbers, then
    convert to scientific notation.

    Complexity
    ----------
    O(m * n) time for the double loop to sum the logarithms, O(1) space.

    References
    ----------
    https://projecteuler.net/problem=380
    """
    m = 100
    n = 500
    sum_log10 = 0.0
    for p in tqdm(range(1, m + 1)):
        arg_p = math.pi * (p - 1) / m
        lp = 2 - 2 * math.cos(arg_p)
        for q in range(1, n + 1):
            arg_q = math.pi * (q - 1) / n
            lq = 2 - 2 * math.cos(arg_q)
            term = lp + lq
            if term > 0:
                sum_log10 += math.log10(term)

    sum_log10 -= math.log10(m * n)
    exponent = math.floor(sum_log10)
    frac = sum_log10 - exponent
    mant = 10 ** frac
    rounded_mant = round(mant, 4)

    if rounded_mant >= 10:
        rounded_mant /= 10
        exponent += 1

    print(f"{rounded_mant:.4f}e{exponent}")

if __name__ == "__main__":
    main()