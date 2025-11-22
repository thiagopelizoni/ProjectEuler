# Problem: https://projecteuler.net/problem=353
import math
from heapq import heappush, heappop
import numba
from numba import njit
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

@njit
def update_dist(d, w, dist, V):
    updated = numba.typed.List()
    for v in range(V):
        new_d = d + w[v]
        if new_d < dist[v]:
            dist[v] = new_d
            updated.append(v)
    return updated

def get_points_chunk(start_x, end_x, r2):
    points = []
    for x in range(start_x, end_x):
        xx = x * x
        max_y = math.isqrt(r2 - xx)
        for y in range(-max_y, max_y + 1):
            yy = y * y
            z2 = r2 - xx - yy
            if z2 >= 0:
                z = math.isqrt(z2)
                if z * z == z2:
                    points.append((x, y, z))
                    if z2 > 0:
                        points.append((x, y, -z))
    return points

def get_points(r):
    r2 = r * r
    with ProcessPoolExecutor() as executor:
        num_cpus = executor._max_workers
        chunk_size = (2 * r + 1) // num_cpus + 1
        futures = []
        start = -r
        for i in range(num_cpus):
            end = min(start + chunk_size, r + 1)
            if start >= end:
                break
            futures.append(executor.submit(get_points_chunk, start, end, r2))
            start = end
        points = []
        for future in as_completed(futures):
            points.extend(future.result())
    return points

def compute_m(r, points):
    V = len(points)
    points_np = np.array(points, dtype=np.float64)
    r2 = np.float64(r * r)
    N = next(i for i, p in enumerate(points) if p[2] == r and p[0] == 0 and p[1] == 0)
    S = next(i for i, p in enumerate(points) if p[2] == -r and p[0] == 0 and p[1] == 0)
    dist = np.full(V, np.inf, dtype=np.float64)
    dist[N] = 0.0
    pq = []
    heappush(pq, (0.0, N))
    visited = np.full(V, False, dtype=np.bool_)
    pbar = tqdm(total=V, desc=f"Dijkstra for r={r}")
    while pq:
        d, u = heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        pbar.update(1)
        if u == S:
            pbar.close()
            return d
        dots = np.dot(points_np, points_np[u])
        cos_theta = dots / r2
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        theta = np.arccos(cos_theta)
        w = (theta / math.pi) ** 2
        w[u] = np.inf  # skip self
        updated = update_dist(d, w, dist, V)
        for v in updated:
            heappush(pq, (dist[v], v))
    pbar.close()
    return dist[S]

def main():
    sum_m = 0.0
    for n in range(1, 16):
        r = (1 << n) - 1
        points = get_points(r)
        m = compute_m(r, points)
        sum_m += m
    print(f"{sum_m:.10f}")

if __name__ == "__main__":
    main()