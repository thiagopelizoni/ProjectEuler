# Problem: https://projecteuler.net/problem=314
import math
import heapq
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def compute_min_cost(s, r):
    if s == 0:
        return 0.0
    band = 4.0
    max_jump = 20
    points = []
    for x in range(s + 1):
        for y in range(s + 1):
            dx = x - s
            dy = y - s
            dist = math.sqrt(dx * dx + dy * dy)
            if abs(dist - s) <= band:
                points.append((x, y))
    start = (s, 0)
    end = (0, s)
    if start not in set(points) or end not in set(points):
        return float('inf')
    dists = defaultdict(lambda: float('inf'))
    dists[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        cost, p = heapq.heappop(pq)
        if cost > dists[p]:
            continue
        x1, y1 = p
        if p == end:
            break
        for qx, qy in points:
            if qx >= x1 or qy <= y1:
                continue
            if abs(qx - x1) > max_jump or abs(qy - y1) > max_jump:
                continue
            length = math.sqrt((x1 - qx) ** 2 + (y1 - qy) ** 2)
            area_contrib = 0.5 * (x1 * qy - qx * y1)
            edge_cost = area_contrib + r * length
            new_cost = cost + edge_cost
            if new_cost < dists[(qx, qy)]:
                dists[(qx, qy)] = new_cost
                heapq.heappush(pq, (new_cost, (qx, qy)))
    return dists[end]

def main():
    low = 125.0
    high = 132.54
    for _ in range(50):
        mid = (low + high) / 2
        with ProcessPoolExecutor() as ex:
            futures = [ex.submit(compute_min_cost, s, mid) for s in range(251)]
            min_costs = [f.result() for f in tqdm(futures, desc="Processing s for mid={:.5f}".format(mid))]
        max_val = float('-inf')
        for s in range(251):
            min_cost = min_costs[s]
            if min_cost == float('inf'):
                continue
            val = 8 * mid * s - 4 * min_cost
            if val > max_val:
                max_val = val
        if 250000 - mid * 2000 + max_val >= 0:
            low = mid
        else:
            high = mid
    print("{:.8f}".format(low))

if __name__ == "__main__":
    main()