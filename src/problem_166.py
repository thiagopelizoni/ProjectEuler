# Problem: https://projecteuler.net/problem=166
def count_configurations():
    total_count = 0

    for a in range(10):
        for b in range(10):
            for c in range(10):
                sum_row1_partial = a + b + c

                for e in range(10):
                    for f in range(10):
                        for g in range(10):
                            sum_row2_partial = e + f + g

                            min_sum_all = sum_row1_partial if sum_row1_partial > sum_row2_partial else sum_row2_partial
                            max_sum_all = (sum_row1_partial + 9) if (sum_row1_partial + 9) < (sum_row2_partial + 9) else (sum_row2_partial + 9)

                            if min_sum_all > max_sum_all:
                                continue

                            for target_sum in range(min_sum_all, max_sum_all + 1):
                                d = target_sum - sum_row1_partial
                                h = target_sum - sum_row2_partial

                                i_min = target_sum - a - e - 9
                                i_max = target_sum - a - e
                                if i_max < 0 or i_min > 9:
                                    continue

                                j_min = target_sum - b - f - 9
                                j_max = target_sum - b - f
                                if j_max < 0 or j_min > 9:
                                    continue

                                k_min = target_sum - c - g - 9
                                k_max = target_sum - c - g
                                if k_max < 0 or k_min > 9:
                                    continue

                                i_low = 0 if i_min < 0 else i_min
                                i_high = 9 if i_max > 9 else i_max

                                j_low = 0 if j_min < 0 else j_min
                                j_high = 9 if j_max > 9 else j_max

                                k_low = 0 if k_min < 0 else k_min
                                k_high = 9 if k_max > 9 else k_max

                                for j in range(j_low, j_high + 1):
                                    i = d + g + j - a - e
                                    if i < i_low or i > i_high:
                                        continue

                                    numerator = target_sum - a - f + d + h - i - j
                                    if numerator & 1:
                                        continue

                                    k = numerator // 2
                                    if k < k_low or k > k_high:
                                        continue

                                    l = target_sum - i - j - k
                                    if l < 0 or l > 9:
                                        continue

                                    m = target_sum - a - e - i
                                    n = target_sum - b - f - j
                                    o = target_sum - c - g - k

                                    if m < 0 or m > 9 or n < 0 or n > 9 or o < 0 or o > 9:
                                        continue

                                    p = target_sum - d - h - l
                                    if p < 0 or p > 9:
                                        continue

                                    total_count += 1

    return total_count

if __name__ == "__main__":
    print(count_configurations())
