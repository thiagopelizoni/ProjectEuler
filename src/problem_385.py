# Problem: https://projecteuler.net/problem=385
import math

def main():
    n = 1000000000
    cases = [
        {"D": 1, "e": 117, "st_list": [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)], "classes": [
            [(12, 3)],
            [(15, 6)]
        ]},
        {"D": 13, "e": 9, "st_list": [(-4, -3), (-4, -1), (-3, -4), (-3, 1), (-1, -4), (-1, 3), (1, -3), (1, 4), (3, -1), (3, 4), (4, 1), (4, 3)], "classes": [
            [(3, 0)]
        ]}
    ]
    total = 0
    for case in cases:
        D = case["D"]
        for class_start in case["classes"]:
            d, k = class_start[0]
            while d <= 4 * 10**9:
                for st in case["st_list"]:
                    s, t = st
                    num_u = d * (2 * s - t)
                    if num_u % 3 != 0:
                        continue
                    u = num_u // 3
                    num_v = d * (-s + 2 * t)
                    if num_v % 3 != 0:
                        continue
                    v = num_v // 3
                    x3 = -u - v
                    max_x = max(abs(u), abs(v), abs(x3))
                    if k == 0:
                        max_y = 0
                    else:
                        max_y = k * max(abs(t), abs(s), abs(t - s))
                    if max_x <= n and max_y <= n:
                        factor = 1 if k == 0 else 2
                        total += factor * k * d * D
                next_d = 2 * d + 3 * k
                next_k = d + 2 * k
                d = next_d
                k = next_k
    print(total // 6)

if __name__ == "__main__":
    main()