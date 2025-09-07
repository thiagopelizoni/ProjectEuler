# Problem: https://projecteuler.net/problem=283
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import floor, sqrt
from tqdm import tqdm

def find_max_e(d: int, k: int) -> int:
    low = 0
    high = (8 * k * k) // max(1, d) + 2 * k + 1
    while low < high:
        mid = (low + high + 1) // 2
        quad = d * mid * mid - 8 * k * k * mid - 4 * k * k * d
        if quad <= 0:
            low = mid
        else:
            high = mid - 1
    return low

def compute_for_k(k: int) -> int:
    total = 0
    m2 = 4 * k * k
    max_d = floor(sqrt(12) * k) + 1
    for d in range(1, max_d + 1):
        lower_e = max(d, m2 // d + 1)
        upper_e = find_max_e(d, k)
        if upper_e < lower_e:
            continue
        for e in range(lower_e, upper_e + 1):
            denom = d * e - m2
            if denom <= 0:
                continue
            num = m2 * (d + e)
            if num % denom == 0:
                f = num // denom
                if f >= e:
                    p = 2 * (d + e + f)
                    total += p
    return total

def main():
    """
    Purpose
    Computes the sum of the perimeters of all integer-sided triangles where the area/perimeter ratio is a positive integer <= 1000.

    Method / Math Rationale
    For each integer k from 1 to 1000, find all positive integers d <= e <= f such that d*e*f = 4*k**2*(d+e+f).
    This parametrizes the Heronian triangles with area/perimeter = k.
    Loop over d=1 to floor(sqrt(12)*k)+1, e from max(d, 4*k**2//d +1) to the largest e where d*e**2 -8*k**2*e -4*k**2*d <=0
    (found via binary search to avoid floating-point issues), compute f = 4*k**2*(d+e) / (d*e - 4*k**2), check if integer and >=e.
    Perimeter = 2*(d+e+f). Sum all such perimeters.

    Complexity
    Time: O(sum_{k=1}^{1000} k^2 log k) ≈ O(10^9) operations, parallelized over k.
    Space: O(1) per process.

    References
    https://projecteuler.net/problem=283
    """
    max_k = 1000
    total_sum = 0
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_for_k, k) for k in range(1, max_k + 1)]
        for future in tqdm(as_completed(futures), total=max_k):
            total_sum += future.result()
    print(total_sum)

if __name__ == "__main__":
    main()