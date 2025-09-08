# Problem: https://projecteuler.net/problem=292
import math
import sys
from collections import namedtuple
from functools import lru_cache
from tqdm import tqdm

sys.setrecursionlimit(10000)

Direction = namedtuple('Direction', ['x', 'y', 'dis'])

max_coordinate = 120

def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a

def check(x, y):
    x = abs(x)
    y = abs(y)
    if x == 0 and y == 0:
        return 0
    if gcd(x, y) != 1:
        return 0
    buf = x * x + y * y
    s = math.isqrt(buf)
    if s * s == buf:
        return s
    return 0

def init_all_dir():
    all_dir = []
    for i in range(0, max_coordinate + 1):
        for j in range(0, max_coordinate + 1):
            d = check(i, j)
            if d > 0:
                all_dir.append(Direction(i, j, d))
    all_dir.sort(key=lambda d: math.atan2(d.y, d.x))
    len1 = len(all_dir)
    for i in range(len1 - 2, -1, -1):
        d = all_dir[i]
        all_dir.append(Direction(-d.x, d.y, d.dis))
    len2 = len(all_dir)
    for i in range(len2 - 2, 0, -1):
        d = all_dir[i]
        all_dir.append(Direction(d.x, -d.y, d.dis))
    return all_dir

all_dir = init_all_dir()

@lru_cache(maxsize=None)
def gao(x, y, len_, ind):
    if x == max_coordinate and y == max_coordinate and len_ == 0:
        return 1
    if len_ <= 0:
        return 0
    res = 0
    for next_ind in range(ind, len(all_dir)):
        dx, dy, dis = all_dir[next_ind]
        if ind > 0 and dx == -all_dir[ind - 1].x and dy == -all_dir[ind - 1].y:
            continue
        max_k = len_ // dis
        for k in range(1, max_k + 1):
            new_x = x + k * dx
            new_y = y + k * dy
            new_len = len_ - k * dis
            if (new_x - max_coordinate) ** 2 + (new_y - max_coordinate) ** 2 > new_len ** 2:
                continue
            res += gao(new_x, new_y, new_len, next_ind + 1)
    return res

def main():
    """
    Purpose
    Computes the number of distinct Pythagorean polygons with perimeter <= 120 as defined in Project Euler problem 292.

    Method / Math Rationale
    Uses dynamic programming with memoization to count convex lattice polygons with integer edge lengths up to translation. Directions are precomputed and sorted by angle to canonicalize rotations by enforcing strictly increasing direction indices. Convexity is maintained by left turns and skipping 180-degree turns. Pruning uses squared distance check against remaining perimeter. Counts exact perimeters for even values and accumulates for <= 120.

    Complexity
    O(number of visited states * number of directions * max_k), optimized by pruning and canonical ordering.

    References
    https://projecteuler.net/problem=292
    """
    total = 0
    for perim in tqdm(range(4, 121, 2)):
        buf = gao(max_coordinate, max_coordinate, perim, 0)
        total += buf
    print(total)

if __name__ == "__main__":
    main()