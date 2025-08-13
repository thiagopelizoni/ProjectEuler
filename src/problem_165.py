# Problem: https://projecteuler.net/problem=165
import numpy as np


def generate_segments(segment_count=5000):
    seed_value = 290797
    x_start = np.empty(segment_count, dtype=np.int64)
    y_start = np.empty(segment_count, dtype=np.int64)
    x_end = np.empty(segment_count, dtype=np.int64)
    y_end = np.empty(segment_count, dtype=np.int64)

    for index in range(segment_count):
        seed_value = (seed_value * seed_value) % 50515093
        x_start[index] = seed_value % 500

        seed_value = (seed_value * seed_value) % 50515093
        y_start[index] = seed_value % 500

        seed_value = (seed_value * seed_value) % 50515093
        x_end[index] = seed_value % 500

        seed_value = (seed_value * seed_value) % 50515093
        y_end[index] = seed_value % 500

    return x_start, y_start, x_end, y_end


def count_distinct_true_intersections(x_start, y_start, x_end, y_end):
    count_segments = x_start.shape[0]

    min_x = np.minimum(x_start, x_end)
    max_x = np.maximum(x_start, x_end)
    min_y = np.minimum(y_start, y_end)
    max_y = np.maximum(y_start, y_end)

    all_x_num = []
    all_y_num = []
    all_den = []

    for i in range(count_segments - 1):
        j_index = np.arange(i + 1, count_segments, dtype=np.int64)

        bbox_overlap = (
            (max_x[i] >= min_x[j_index])
            & (max_x[j_index] >= min_x[i])
            & (max_y[i] >= min_y[j_index])
            & (max_y[j_index] >= min_y[i])
        )

        if not np.any(bbox_overlap):
            continue

        j_sel = j_index[bbox_overlap]

        xs1 = x_start[j_sel]
        ys1 = y_start[j_sel]
        xs2 = x_end[j_sel]
        ys2 = y_end[j_sel]

        dx_p = x_end[i] - x_start[i]
        dy_p = y_end[i] - y_start[i]

        cross1 = dx_p * (ys1 - y_start[i]) - dy_p * (xs1 - x_start[i])
        cross2 = dx_p * (ys2 - y_start[i]) - dy_p * (xs2 - x_start[i])

        cond_12 = (cross1 != 0) & (cross2 != 0) & (
            (cross1 > 0) != (cross2 > 0)
        )

        if not np.any(cond_12):
            continue

        xs1 = xs1[cond_12]
        ys1 = ys1[cond_12]
        xs2 = xs2[cond_12]
        ys2 = ys2[cond_12]

        dx_q = xs2 - xs1
        dy_q = ys2 - ys1

        cross3 = dx_q * (y_start[i] - ys1) - dy_q * (x_start[i] - xs1)
        cross4 = dx_q * (y_end[i] - ys1) - dy_q * (x_end[i] - xs1)

        cond_34 = (cross3 != 0) & (cross4 != 0) & (
            (cross3 > 0) != (cross4 > 0)
        )

        if not np.any(cond_34):
            continue

        xs1 = xs1[cond_34]
        ys1 = ys1[cond_34]
        xs2 = xs2[cond_34]
        ys2 = ys2[cond_34]

        a1 = y_start[i] - y_end[i]
        b1 = x_end[i] - x_start[i]
        c1 = x_start[i] * y_end[i] - x_end[i] * y_start[i]

        a2 = ys1 - ys2
        b2 = xs2 - xs1
        c2 = xs1 * ys2 - xs2 * ys1

        den = a1 * b2 - a2 * b1
        x_num = c1 * b2 - c2 * b1
        y_num = a1 * c2 - a2 * c1

        need_flip = den < 0
        if np.any(need_flip):
            den = np.where(need_flip, -den, den)
            x_num = np.where(need_flip, -x_num, x_num)
            y_num = np.where(need_flip, -y_num, y_num)

        gcd_xy = np.gcd(np.abs(x_num), np.abs(y_num))
        gcd_all = np.gcd(gcd_xy, den)

        x_num = x_num // gcd_all
        y_num = y_num // gcd_all
        den = den // gcd_all

        all_x_num.append(x_num)
        all_y_num.append(y_num)
        all_den.append(den)

    if not all_x_num:
        return 0

    x_num = np.concatenate(all_x_num)
    y_num = np.concatenate(all_y_num)
    den = np.concatenate(all_den)

    triples = np.stack((x_num, y_num, den), axis=1)
    dtype = np.dtype([("x", np.int64), ("y", np.int64), ("d", np.int64)])
    structured = triples.view(dtype).reshape(-1)

    unique_points = np.unique(structured).size
    return int(unique_points)


def solve():
    x_start, y_start, x_end, y_end = generate_segments(5000)
    result = count_distinct_true_intersections(
        x_start,
        y_start,
        x_end,
        y_end,
    )
    return result


print(solve())
