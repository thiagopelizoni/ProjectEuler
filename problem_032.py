# Problem: https://projecteuler.net/problem=32
def is_pandigital(n, s=9):
    return len(n) == s and not '1234567890'[:s].strip(n)

if __name__ == "__main__":
    pandigital_products = set()

    for i in range(2, 100):
        start = 1234 if i < 10 else 123
        for j in range(start, 10000 // i):
            if is_pandigital(str(i) + str(j) + str(i * j)):
                pandigital_products.add(i * j)

    answer = sum(pandigital_products)
    print(answer)
