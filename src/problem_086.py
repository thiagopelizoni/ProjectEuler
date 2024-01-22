# Problem: https://projecteuler.net/problem=86
def find_least_value_of_m(limit):
    solutions = 0
    M = 0

    while solutions < limit:
        M += 1
        for x in range(1, 2 * M + 1):
            sqrt_val = (M * M + x * x) ** 0.5
            if sqrt_val.is_integer():
                if x <= M:
                    solutions += x // 2

                else:
                    solutions += 1 + (M - (x + 1) // 2)

    return M

if __name__ == "__main__":
    answer = find_least_value_of_m(1_000_000)
    print(answer)
