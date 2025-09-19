# Problem: https://projecteuler.net/problem=332
import math
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def get_points(r):
    points = []
    rsq = r * r
    for x in range(-r, r + 1):
        xsq = x * x
        for y in range(-r, r + 1):
            ysq = y * y
            zsq = rsq - xsq - ysq
            if zsq >= 0:
                z = math.isqrt(zsq)
                if z * z == zsq:
                    points.append((x, y, z))
                    if z > 0:
                        points.append((x, y, -z))
    return points

def compute_A(r):
    points = get_points(r)
    n = len(points)
    if n < 3:
        return 0.0
    rsq = r * r
    min_area = float('inf')
    for triplet in tqdm(itertools.combinations(points, 3), total=math.comb(n, 3)):
        A, B, C = triplet
        dotAB = A[0]*B[0] + A[1]*B[1] + A[2]*B[2]
        dotAC = A[0]*C[0] + A[1]*C[1] + A[2]*C[2]
        dotBC = B[0]*C[0] + B[1]*C[1] + B[2]*C[2]
        bxcy = B[1]*C[2] - B[2]*C[1]
        bxcz = B[2]*C[0] - B[0]*C[2]
        bxcx = B[0]*C[1] - B[1]*C[0]
        det = A[0]*bxcy + A[1]*bxcz + A[2]*bxcx
        if det == 0:
            continue
        denom = r**3 + r * (dotAB + dotAC + dotBC)
        omega = 2 * math.atan2(abs(det), denom)
        area = rsq * omega
        area = min(area, 4 * math.pi * rsq - area)
        if area < min_area:
            min_area = area
    return min_area

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 332 by computing the sum of the minimal areas of spherical triangles
    formed by lattice points on spheres of radii 1 to 50.

    Method / Math Rationale
    -----------------------
    For each radius r, generate all lattice points on the sphere x² + y² + z² = r². Then, for all
    combinations of three points, check if non-degenerate (scalar triple product ≠ 0), compute the
    solid angle using omega = 2 * atan2(|det|, denom), where denom = r³ + r*(dotAB + dotAC + dotBC),
    take the smaller area via min(rsq * omega, 4*pi*rsq - rsq * omega).

    Complexity
    ----------
    O( sum_{r=1}^{50} binom{N(r)}{3} ), where N(r) is number of lattice points, up to ~500k per r,
    total ~10^7 operations.

    References
    ----------
    https://projecteuler.net/problem=332
    """
    total = 0.0
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_A, r) for r in range(1, 51)]
        for future in as_completed(futures):
            total += future.result()
    print(f"{total:.6f}")

if __name__ == "__main__":
    main()