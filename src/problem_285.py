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
    total: float = 0.0
    N: int = 100000
    for k in tqdm(range(1, N + 1)):
        area: float = compute_area(k + 0.5) - compute_area(k - 0.5)
        total += area / k
    print(f"{total:.5f}")

if __name__ == "__main__":
    main()