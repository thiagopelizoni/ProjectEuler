# Problem: https://projecteuler.net/problem=509
def main():
    n = 123456787654321
    mod = 1234567890
    counts = [0] * 64
    counts[0] = (n + 1) // 2
    k = 1
    power = 2
    while True:
        div = n // power
        if div == 0:
            break
        counts[k] = (div + 1) // 2
        k += 1
        power *= 2
        if k >= 64:
            break
    max_k = k - 1
    losing = 0
    for i in range(max_k + 1):
        ci = counts[i] % mod
        for j in range(max_k + 1):
            cj = counts[j] % mod
            for l in range(max_k + 1):
                if (i ^ j ^ l) == 0:
                    cl = counts[l] % mod
                    add = (ci * cj % mod) * cl % mod
                    losing = (losing + add) % mod
    total = pow(n, 3, mod)
    result = (total - losing + mod) % mod
    print(result)

if __name__ == "__main__":
    main()