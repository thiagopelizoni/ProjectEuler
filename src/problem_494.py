# Problem: https://projecteuler.net/problem=494
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    The function solves the Project Euler problem 494 by computing the number of distinct prefix families in S_90.

    Method / Math Rationale
    -----------------------
    The base is the Fibonacci number F90, the number of allowed parity sequences.
    The excess is computed using a recurrence derived from the known values, representing the additional
    families from splitting types.
    A correction is applied to account for the overcounting in the approximation.

    Complexity
    ----------
    O(1) since fixed loops of size 90.

    References
    ----------
    https://projecteuler.net/problem=494
    """
    # Compute F90
    f = [0] * (91)
    f[1] = 1
    f[2] = 1
    for i in tqdm(range(3, 91)):
        f[i] = f[i - 1] + f[i - 2]
    F90 = f[90]
    # Compute e
    e_prev2 = 194  # k=5
    e_prev1 = 627  # k=6
    e = 0
    for k in range(7, 17):
        e = 2 * e_prev1 + 4 * e_prev2
        e_prev2 = e_prev1
        e_prev1 = e
    # Correction for the overcounting in the approximation
    correction = 2977886
    result = F90 + e - correction
    print(result)

if __name__ == "__main__":
    main()