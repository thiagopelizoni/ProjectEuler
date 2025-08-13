# Problem: https://projecteuler.net/problem=163
def count_triangles(size: int) -> int:
    term_a = 1678 * size ** 3
    term_b = 3117 * size ** 2
    term_c = 88 * size

    mod2 = (size % 2) * 345
    mod3 = (size % 3) * 320
    mod4 = (size % 4) * 90
    mod5 = ((size ** 3 - size ** 2 + size) % 5) * 288

    numerator = term_a + term_b + term_c - mod2 - mod3 - mod4 - mod5
    result = numerator // 240

    return result

if __name__ == "__main__":
    print(count_triangles(36))
