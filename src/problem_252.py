# Problem: https://projecteuler.net/problem=252
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from numba import njit


@njit(fastmath=True)
def solve_for_subset(origin, sorted_pts):
    m = len(sorted_pts)
    if m < 2:
        return 0.0

    is_empty = np.ones((m, m), dtype=np.bool_)

    for k in range(2, m):
        for j in range(k - 1):
            for r in range(j + 1, k):
                cp = (sorted_pts[k][0] - sorted_pts[j][0]) * (sorted_pts[r][1] - sorted_pts[j][1]) - \
                     (sorted_pts[k][1] - sorted_pts[j][1]) * (sorted_pts[r][0] - sorted_pts[j][0])
                if cp > 0:
                    is_empty[j, k] = False
                    break

    dp = np.zeros((m, m), dtype=np.float64)
    global_max = 0.0

    for k in range(1, m):
        for j in range(k):
            if not is_empty[j, k]:
                continue

            cp_val = (sorted_pts[j][0] * sorted_pts[k][1] - sorted_pts[j][1] * sorted_pts[k][0])
            area = 0.5 * abs(cp_val)

            best_prev = 0.0

            for u in range(j):
                vec_uj_x = sorted_pts[j][0] - sorted_pts[u][0]
                vec_uj_y = sorted_pts[j][1] - sorted_pts[u][1]
                vec_jk_x = sorted_pts[k][0] - sorted_pts[j][0]
                vec_jk_y = sorted_pts[k][1] - sorted_pts[j][1]
                cross_turn = vec_uj_x * vec_jk_y - vec_uj_y * vec_jk_x

                if cross_turn > 0:
                    if dp[u, j] > best_prev:
                        best_prev = dp[u, j]

            if best_prev > 0:
                dp[j, k] = best_prev + area
            else:
                dp[j, k] = area

            if dp[j, k] > global_max:
                global_max = dp[j, k]

    return global_max


def worker(args):
    idx, all_points = args
    origin = all_points[idx]

    others = []
    origin_x, origin_y = origin

    for i in range(len(all_points)):
        if i == idx:
            continue
        px, py = all_points[i]
        dx = px - origin_x
        dy = py - origin_y
        if dy > 0 or (dy == 0 and dx > 0):
            others.append((dx, dy))

    if not others:
        return 0.0

    others_np = np.array(others, dtype=np.float64)
    angles = np.arctan2(others_np[:, 1], others_np[:, 0])
    sorted_indices = np.argsort(angles)
    sorted_pts = others_np[sorted_indices]

    return solve_for_subset(np.array([0.0, 0.0], dtype=np.float64), sorted_pts)


def main():
    S = 290797
    mod = 50515093
    T = []

    for _ in range(1000):
        S = (S * S) % mod
        T_val = (S % 2000) - 1000
        T.append(T_val)

    points = []
    for k in range(500):
        points.append((T[2 * k], T[2 * k + 1]))

    points_np = np.array(points, dtype=np.float64)
    N = len(points)
    tasks = [(i, points_np) for i in range(N)]

    max_area = 0.0

    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(worker, tasks), total=N, unit="anchor"))

    max_area = max(results)

    print(f"{max_area:.1f}")


if __name__ == "__main__":
    main()