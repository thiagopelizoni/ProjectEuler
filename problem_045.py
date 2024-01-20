# Problem: https://projecteuler.net/problem=45
def is_pentagonal(n):
    """Check if a number is pentagonal."""
    pen_test = (1 + (1 + 24 * n)**0.5) / 6
    return pen_test.is_integer()

def is_hexagonal(n):
    """Check if a number is hexagonal."""
    hex_test = (1 + (1 + 8 * n)**0.5) / 4
    return hex_test.is_integer()

def answer():
    i = 286
    while True:
        triangle = i * (i + 1) // 2
        if is_pentagonal(triangle) and is_hexagonal(triangle):
            return triangle
        i += 1

print(answer())
