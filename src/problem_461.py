# Problem: https://projecteuler.net/problem=461
import math
from bisect import bisect_right
from tqdm import tqdm

def main():
    n = 10000
    pi = math.pi
    f = []
    k = 0
    while True:
        current = math.exp(k / n) - 1
        if current > pi:
            break
        f.append(current)
        k += 1
    maximum = len(f)
    pairs = []
    for i in tqdm(range(maximum)):
        for j in range(i, maximum):
            s = f[i] + f[j]
            if s > pi:
                break
            pairs.append(s)
    pairs.sort()
    min_error = pi
    left = 0
    right = 0
    for idx in range(len(pairs)):
        current = pairs[idx]
        need = pi - current
        if need < current:
            break
        pos = bisect_right(pairs, need)
        for p in [pos, pos - 1]:
            if 0 <= p < len(pairs):
                error = abs(need - pairs[p])
                if error < min_error:
                    min_error = error
                    left = idx
                    right = p
    # resolve left
    sum_left = pairs[left]
    a = b = None
    for i in range(maximum):
        for j in range(i, maximum):
            if abs(f[i] + f[j] - sum_left) < 1e-12:
                a = i
                b = j
                goto_next = True
                break
        if a is not None:
            break
    # resolve right
    sum_right = pairs[right]
    c = d = None
    for i in range(maximum):
        for j in range(i, maximum):
            if abs(f[i] + f[j] - sum_right) < 1e-12:
                c = i
                d = j
                break
        if c is not None:
            break
    g = a**2 + b**2 + c**2 + d**2
    print(g)

if __name__ == "__main__":
    main()