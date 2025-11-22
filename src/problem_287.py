# Problem: https://projecteuler.net/problem=287
import sys
import numba

sys.setrecursionlimit(100000)

@numba.njit
def compute_length(min_x: int, min_y: int, size: int, cx: int, cy: int,
                   r2: int) -> int:
    x1 = min_x
    x2 = min_x + size - 1
    y1 = min_y
    y2 = min_y + size - 1
    d1 = (x1 - cx) ** 2 + (y1 - cy) ** 2
    d2 = (x1 - cx) ** 2 + (y2 - cy) ** 2
    d3 = (x2 - cx) ** 2 + (y1 - cy) ** 2
    d4 = (x2 - cx) ** 2 + (y2 - cy) ** 2
    max_d2 = max(d1, d2, d3, d4)
    px = max(x1, min(cx, x2))
    py = max(y1, min(cy, y2))
    min_d2 = (px - cx) ** 2 + (py - cy) ** 2
    if max_d2 <= r2:
        return 2
    elif min_d2 > r2:
        return 2
    else:
        half = size // 2
        tl = compute_length(min_x, min_y + half, half, cx, cy, r2)
        tr = compute_length(min_x + half, min_y + half, half, cx, cy, r2)
        bl = compute_length(min_x, min_y, half, cx, cy, r2)
        br = compute_length(min_x + half, min_y, half, cx, cy, r2)
        return 1 + tl + tr + bl + br

def main():
    n = 24
    size = 1 << n
    cx = 1 << (n - 1)
    cy = cx
    r2 = 1 << (2 * n - 2)
    length = compute_length(0, 0, size, cx, cy, r2)
    print(length)

if __name__ == "__main__":
    main()