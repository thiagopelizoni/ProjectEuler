# Problem: https://projecteuler.net/problem=285
from math import asin, sqrt
from tqdm import tqdm

def compute_area(R: float) -> float:
    if R <= sqrt(2):
        return 0.0
    rsq = R * R
    s = sqrt(rsq - 1.0)
    def F(u: float) -> float:
        sqrt_term = sqrt(rsq - u**2)
        return 0.5 * u * sqrt_term + 0.5 * rsq * asin(u / R) - u
    return F(s) - F(1.0)

def main():
    """
    Purpose
    Computes the expected value of Albert's total score for k=1 to 10^5, rounded to five decimal places.

    Args
    None

    Returns
    None

    Method / Math Rationale
    For each k, the probability p_k is the area in the (u,v)-plane [1,k+1]^2 where (k-0.5)^2 <= u^2 + v^2 < (k+0.5)^2,
    divided by k^2. The expected score per k is area / k. The area is computed as the difference of two cap areas,
    each found by integrating (sqrt(R^2 - u^2) - 1) from 1 to sqrt(R^2 - 1), using the antiderivative
    (1/2)u sqrt(R^2 - u^2) + (1/2)R^2 arcsin(u/R) - u. Sum these contributions over k=1 to 10^5.

    Complexity
    Time: O(N) with N=10^5 for the loop over k. Space: O(1).

    References
    https://projecteuler.net/problem=285
    """
    total: float = 0.0
    N: int = 100000
    for k in tqdm(range(1, N + 1)):
        area: float = compute_area(k + 0.5) - compute_area(k - 0.5)
        total += area / k
    print(f"{total:.5f}")

if __name__ == "__main__":
    main()