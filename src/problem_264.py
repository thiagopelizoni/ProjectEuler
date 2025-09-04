# Problem: https://projecteuler.net/problem=264
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import sqrt
from tqdm import tqdm

max_d = 1000000000

def is_square(n):
    if n < 0:
        return False
    s = int(sqrt(n))
    return s * s == n

def compute_dist(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_perimeter(p1, p2, p3):
    return compute_dist(*p1, *p2) + compute_dist(*p2, *p3) + compute_dist(*p3, *p1)

def process_chunk(x_start, x_end):
    triangles = []
    max_r = int(sqrt(max_d)) + 1
    for x1 in range(x_start, x_end):
        max_y = int(sqrt(max_d - x1 * x1))
        for y1 in range(-max_y, max_y + 1):
            d = x1 * x1 + y1 * y1
            if d == 0:
                continue
            vx = x1 - 5
            vy = y1
            vv = vx * vx + vy * vy
            if vv % 2 != 0 or vv == 0:
                continue
            k = -vv // 2
            found_p = []
            if vy == 0:
                if k % vx == 0:
                    px = k // vx
                    pp = d - px * px
                    if pp >= 0 and is_square(pp):
                        m = int(sqrt(pp))
                        found_p.append((px, m))
                        found_p.append((px, -m))
            else:
                disc = 4 * vy * vy * (vv * d - k * k)
                if disc >= 0 and is_square(disc):
                    s = int(sqrt(disc))
                    for sign in [1, -1]:
                        num = 2 * k * vx + sign * s
                        den = 2 * vv
                        if num % den == 0:
                            px = num // den
                            num_py = k - px * vx
                            if num_py % vy == 0:
                                py = num_py // vy
                                if px * px + py * py == d:
                                    found_p.append((px, py))
            for px, py in found_p:
                cx = 5 - x1 - px
                cy = -y1 - py
                if (px, py) == (x1, y1) or (cx, cy) == (x1, y1) or (cx, cy) == (px, py):
                    continue
                if cx * cx + cy * cy != d:
                    continue
                points = sorted([(x1, y1), (px, py), (cx, cy)])
                per = get_perimeter(points[0], points[1], points[2])
                if per <= 100000:
                    key = frozenset(points)
                    triangles.append((per, key))
    return triangles

if __name__ == "__main__":
    all_triangles = {}
    special_ps = [(0, 5), (3, 4), (-3, 4), (4, 3), (-4, 3)]
    for special_p in special_ps:
        px, py = special_p
        cx = -px
        cy = -py
        hx = 5
        hy = 0
        points = sorted([(hx, hy), (px, py), (cx, cy)])
        key = frozenset(points)
        per = get_perimeter((hx, hy), (px, py), (cx, cy))
        if per <= 100000:
            all_triangles[key] = per
    max_r = int(sqrt(max_d)) + 1
    cpu_count = os.cpu_count()
    chunk_size = (2 * max_r // cpu_count) + 1
    ranges = []
    start = -max_r
    while start <= max_r:
        end = min(start + chunk_size, max_r + 1)
        ranges.append((start, end))
        start = end
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = [executor.submit(process_chunk, low, high) for low, high in ranges]
        for future in tqdm(as_completed(futures), total=len(futures)):
            chunk_tri = future.result()
            for per, key in chunk_tri:
                if key not in all_triangles:
                    all_triangles[key] = per
    total = sum(all_triangles.values())
    print(round(total, 4))