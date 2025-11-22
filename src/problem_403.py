# Problem: https://projecteuler.net/problem=403
import math
from tqdm import tqdm

def compute_sum_k3(A, B):
    if A > B:
        return 0
    sum_B = (B * (B + 1) // 2) ** 2
    sum_A_minus_1 = ((A - 1) * A // 2) ** 2
    return sum_B - sum_A_minus_1

def compute_sum_k2(A, B):
    if A > B:
        return 0
    sum_B = B * (B + 1) * (2 * B + 1) // 6
    sum_A_minus_1 = (A - 1) * A * (2 * A - 1) // 6
    return sum_B - sum_A_minus_1

def compute_sum_k(A, B):
    if A > B:
        return 0
    num = B - A + 1
    return num * (A + B) // 2

def compute_total_add(A, B):
    sum_k3 = compute_sum_k3(A, B)
    sum_k = compute_sum_k(A, B)
    sum_1 = B - A + 1 if A <= B else 0
    return sum_k3 + 5 * sum_k + 6 * sum_1

def main():
    N = 10**12
    MOD = 10**8
    S = int(math.sqrt(N))
    total = 0

    # b >= 0, s = 0
    total += compute_total_add(0, N) + compute_total_add(1, N)

    # b >= 0, small s >= 1
    for s in tqdm(range(1, S + 1)):
        T = N // s
        if T < s:
            continue
        A = 2 * s
        B = s + T
        sum1 = compute_total_add(A, B)
        sum2 = compute_total_add(A + 1, B) if A + 1 <= B else 0
        total += sum1 + sum2

    # b < 0, small s
    for s in range(1, S + 1):
        R = min(s, N // s, N - s)
        if R <= 0:
            continue
        C = s - R
        D = s - 1
        sum3 = compute_total_add(C, D)
        total += 2 * sum3

    # b < 0, large s grouped by m
    for m in tqdm(range(1, S + 1)):
        l = N // (m + 1) + 1
        h = N // m
        if l > h:
            continue
        l = max(l, S + 1)
        if l > h:
            continue
        s_split = N - m
        sumj = m * (m + 1) // 2
        sumj2 = m * (m + 1) * (2 * m + 1) // 6
        sumj3 = sumj ** 2
        coeff_s3 = 2 * m
        coeff_s2 = 2 * (-3 * sumj)
        coeff_s1 = 2 * (3 * sumj2 + 5 * m)
        coeff_const = 2 * (-sumj3 - 5 * sumj + 6 * m)
        if s_split < l:
            for s in range(l, h + 1):
                R = N - s
                if R <= 0:
                    continue
                C = 2 * s - N
                D = s - 1
                sum3 = compute_total_add(C, D)
                total += 2 * sum3
        elif s_split > h:
            sum_s3 = compute_sum_k3(l, h)
            sum_s2 = compute_sum_k2(l, h)
            sum_s = compute_sum_k(l, h)
            num = h - l + 1
            contrib = coeff_s3 * sum_s3 + coeff_s2 * sum_s2 + coeff_s1 * sum_s + coeff_const * num
            total += contrib
        else:
            sum_s3 = compute_sum_k3(l, s_split)
            sum_s2 = compute_sum_k2(l, s_split)
            sum_s = compute_sum_k(l, s_split)
            num1 = s_split - l + 1
            contrib1 = coeff_s3 * sum_s3 + coeff_s2 * sum_s2 + coeff_s1 * sum_s + coeff_const * num1
            total += contrib1
            for s in range(s_split + 1, h + 1):
                R = N - s
                if R <= 0:
                    continue
                C = 2 * s - N
                D = s - 1
                sum3 = compute_total_add(C, D)
                total += 2 * sum3

    ans = (total // 6) % MOD
    print(ans)

if __name__ == "__main__":
    main()