# Problem: https://projecteuler.net/problem=353
import numpy as np
from numba import njit
from math import sqrt, acos, pi
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from sympy import divisors

@njit
def get_points_for_z(z, r):
    points = []
    m = r * r - z * z
    if m < 0:
        return points
    sm = int(sqrt(m) + 0.0001)
    for x in range(-sm, sm + 1):
        yy = m - x * x
        if yy < 0:
            continue
        y = int(sqrt(yy) + 0.0001)
        if y * y == yy:
            points.append(np.array([x, y, z]))
            if y != 0:
                points.append(np.array([x, -y, z]))
    return points

@njit
def dijkstra(points, r, start, goal):
    V = points.shape[0]
    inf = np.inf
    dist = np.full(V, inf)
    dist[start] = 0.0
    visited = np.full(V, False)
    r2 = float(r * r)
    for _ in range(V):
        min_d = inf
        u = -1
        for i in range(V):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        pu = points[u]
        for v in range(V):
            if visited[v]:
                continue
            pv = points[v]
            dot = pu[0] * pv[0] + pu[1] * pv[1] + pu[2] * pv[2]
            cos = dot / r2
            if cos > 1.0:
                cos = 1.0
            if cos < -1.0:
                cos = -1.0
            theta = acos(cos)
            w = (theta / pi) ** 2
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
    return dist[goal]

def compute_m(n):
    r = (1 << n) - 1
    points = []
    future_to_z = {}
    with ProcessPoolExecutor() as executor:
        for z in range(r + 1):
            future_to_z[executor.submit(get_points_for_z, z, r)] = z
        for future in tqdm(as_completed(future_to_z), total=len(future_to_z)):
            z = future_to_z[future]
            pos_points = future.result()
            points.extend(pos_points)
            if z > 0:
                neg_points = [p.copy() for p in pos_points]
                for p in neg_points:
                    p[2] = -p[2]
                points.extend(neg_points)
    points_arr = np.array(points)
    V = points_arr.shape[0]
    N_idx = None
    S_idx = None
    for i in range(V):
        if points_arr[i, 0] == 0 and points_arr[i, 1] == 0 and points_arr[i, 2] == r:
            N_idx = i
        if points_arr[i, 0] == 0 and points_arr[i, 1] == 0 and points_arr[i, 2] == -r:
            S_idx = i
    m = dijkstra(points_arr, r, N_idx, S_idx)
    return m

def main():
    """
    Purpose
    --------
    Solves Project Euler problem 353 by computing the sum of minimal risks M(r) for r = 2^n - 1, n=1 to 15, rounded to 10 decimal places.

    Method / Math Rationale
    -----------------------
    For each r, enumerate integer points on the sphere x^2 + y^2 + z^2 = r^2. Model as a complete graph with edge weights (acos(dot(P, Q) / r^2) / π)^2. Compute shortest path from North Pole (0,0,r) to South Pole (0,0,-r) using Dijkstra's algorithm. Sum M(r) over specified n.

    Complexity
    ----------
    O(V^2) per r where V ≤ 1.7e5, parallelized over n=1 to 15.

    References
    ----------
    https://projecteuler.net/problem=353
    """
    sum_m = 0.0
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_m, n) for n in range(1, 16)]
        for future in tqdm(as_completed(futures), total=15):
            sum_m += future.result()
    print(f"{sum_m:.10f}")

if __name__ == "__main__":
    main()