# Problem: https://projecteuler.net/problem=385
import math

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 385: computes the sum of areas A(n) for n=1000000000, where A(n) is the sum of areas of all integer-coordinate triangles with vertices in [-n,n] x [-n,n] such that the foci of their Steiner inellipse are at (+/-sqrt(13), 0).

    Method / Math Rationale
    ------------------------
    Using Marden's theorem, the condition on foci leads to the vertices satisfying sum z_i = 0 and sum z_i z_j = -39 for complex z_i representing vertices. This translates to sum x=0, sum y=0, sum x y=0, sum(x^2 - y^2)=78. Parameterizing via two vertices determines the third. The conditions reduce to Diophantine equations d^2 - 3 k^2 = e for specific e, solved using recurrences from the fundamental unit of Q(sqrt(3)). For each solution and each direction (s', t'), check if coordinates are integers and within bounds, accumulate contributions accounting for multiplicities.

    Complexity
    ----------
    O(log n) due to generating O(log n) terms in each Pell-like sequence up to size proportional to n.

    References
    ----------
    https://projecteuler.net/problem=385
    https://en.wikipedia.org/wiki/Steiner_inellipse
    https://en.wikipedia.org/wiki/Marden%27s_theorem
    """
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