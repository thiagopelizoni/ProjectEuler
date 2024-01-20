# Problem: https://projecteuler.net/problem=9

def pythagorean_triplet_product(sum_of_triplet):
    for a in range(1, sum_of_triplet):
        for b in range(a, sum_of_triplet - a):
            c = sum_of_triplet - a - b
            if a * a + b * b == c * c:
                return a * b * c
    return None

if __name__ == "__main__":
    answer = pythagorean_triplet_product(1000)
    print(answer)
