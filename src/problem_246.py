# Problem: https://projecteuler.net/problem=246
import math
import sys
from tqdm import tqdm


def main():
    a = 7500
    b_sq = 31250000
    a_sq = 56250000
    dir_r_sq = a_sq + b_sq
    term_s1_const = dir_r_sq
    term_s2_const = a_sq * b_sq
    total_count = 0
    x_limit = 20000

    for x in tqdm(range(x_limit), desc="Scanning x", file=sys.stderr):
        x2 = x * x

        if x2 > a_sq:
            y_min = 0
        else:
            val = math.sqrt(a_sq - x2) * math.sqrt(b_sq) / a
            y_min = math.floor(val) + 1

        if x2 >= dir_r_sq:
            low = 0
        else:
            low = math.ceil(math.sqrt(dir_r_sq - x2))

        high = 25000
        y_max = -1
        s2_base = b_sq * x2 - term_s2_const
        s1_base = x2 - term_s1_const
        y2_low = low * low
        s1_low = s1_base + y2_low
        s2_low = s2_base + a_sq * y2_low
        l_low = (s1_low * s1_low) - 4 * s2_low

        if l_low > 0:
            y_max = -1
        else:
            ans = low
            l, r = low, high
            while l <= r:
                mid = (l + r) // 2
                y2 = mid * mid
                s1 = s1_base + y2
                s2 = s2_base + a_sq * y2
                val = (s1 * s1) - 4 * s2

                if val <= 0:
                    ans = mid
                    l = mid + 1
                else:
                    r = mid - 1
            y_max = ans

        if y_max >= y_min:
            count = y_max - y_min + 1
            has_zero = (y_min == 0)
            if has_zero:
                col_points = 1 + 2 * (count - 1)
            else:
                col_points = 2 * count

            if x == 0:
                total_count += col_points
            else:
                total_count += 2 * col_points

        if x > 10000 and y_max < y_min:
            break

    print(total_count)


if __name__ == "__main__":
    main()