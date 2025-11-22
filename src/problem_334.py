# Problem: https://projecteuler.net/problem=334
def sum_squares(a, b):
    def sum_to(n):
        if n < 0:
            return 0
        return n * (n + 1) * (2 * n + 1) // 6

    if a > b:
        return 0
    if a >= 0:
        return sum_to(b) - sum_to(a - 1)
    if b < 0:
        return sum_to(-a) - sum_to(-b - 1)
    # a < 0 <= b
    return sum_to(-a) + sum_to(b)

def main():
    t = 123456
    b = []
    for _ in range(1500):
        if t % 2 == 0:
            t = t // 2
        else:
            t = t // 2 ^ 926252
        b.append(t % 2048 + 1)

    S = 0
    M = 0
    sum_j2_c = 0
    for i in range(1, 1501):
        bi = b[i - 1]
        S += bi
        M += bi * i
        sum_j2_c += bi * i * i

    # Check if consecutive
    consecutive = False
    L = 0
    if S != 0 and (2 * M) % S == 0:
        temp = (2 * M // S) - S + 1
        if temp % 2 == 0:
            L = temp // 2
            R = L + S - 1
            consecutive = True

    if not consecutive:
        m = M / S
        ideal_L = m - S / 2
        L = round(ideal_L)
        R = L + S
        length = S + 1
        sum_interval = length * (L + R) // 2
        excluded = sum_interval - M
        if not (L <= excluded <= R):
            if ideal_L < L:
                L -= 1
            else:
                L += 1
            R = L + S
            sum_interval = length * (L + R) // 2
            excluded = sum_interval - M
        sum_j2_f = sum_squares(L, R) - excluded * excluded
    else:
        sum_j2_f = sum_squares(L, R)

    answer = (sum_j2_f - sum_j2_c) // 2
    print(answer)

if __name__ == "__main__":
    main()