# Problem: https://projecteuler.net/problem=44

def pentagonal(n):
    return n * (3 * n - 1) // 2

def is_pentagonal(x):
    n = (1 + (1 + 24 * x)**0.5) / 6
    return n.is_integer()

def find_pentagonal():
    i = 1
    while True:
        penta_i = pentagonal(i)
        for j in range(1, i):
            penta_j = pentagonal(j)
            if is_pentagonal(penta_i - penta_j) and is_pentagonal(penta_i + penta_j):
                return penta_i - penta_j
        i += 1

if __name__ == "__main__":
    answer = find_pentagonal()
    print(answer)
