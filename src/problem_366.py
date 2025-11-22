# Problem: https://projecteuler.net/problem=366
def main():
    N = 10**18
    MOD = 10**8

    L = []
    a, b = 1, 2

    while a <= N:
        L.append(a)
        a, b = b, a + b

    num_intervals = len(L)
    p = [0] * (num_intervals + 1)
    l = [0] * (num_intervals + 1)
    sum_s = [0] * (num_intervals + 1)
    p[3] = 1
    p[4] = 2

    for k in range(3, num_intervals + 1):
        l[k] = L[k - 2] - 1

    for k in range(5, num_intervals + 1):
        d = 0 if k % 3 == 2 else 1
        p[k] = p[k - 1] + p[k - 2] + d

    for k in range(3, num_intervals + 1):
        if k == 3 or k == 4:
            sum_s[3] = 1
            sum_s[4] = 1 + 2
            continue
        r = p[k] - l[k - 1] - 1
        sum_prefix = p[k] * (p[k] + 1) // 2
        sum_r = r * (r + 1) // 2
        sum_s[k] = sum_prefix + sum_s[k - 2] - sum_r

    total = 0

    for k in range(3, num_intervals):
        total += sum_s[k]

    # Last interval
    last_l = L[-1]
    num = N - last_l

    # Since num < p[num_intervals], sum 1 to num
    partial = num * (num + 1) // 2

    total += partial
    print(total % MOD)

if __name__ == "__main__":
    main()