# Problem: https://projecteuler.net/problem=135
def main():
    LIMIT = 10**6
    solutions = [0] * LIMIT
    for m in range(1, LIMIT * 2):
        for k in range(m // 5 + 1, (m + 1) // 2):
            temp = (m - k) * (k * 5 - m)
            if temp >= LIMIT:
                break
            solutions[temp] += 1

    result = solutions.count(10)
    return str(result)

if __name__ == "__main__":
    print(main())