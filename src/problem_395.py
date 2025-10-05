# Problem: https://projecteuler.net/problem=395
from decimal import Decimal, getcontext
from tqdm import tqdm

getcontext().prec = 50

class Square:
    def __init__(self, p1x, p1y, p2x, p2y):
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y
        self.length = ((p2x - p1x) ** 2 + (p2y - p1y) ** 2).sqrt()

    def spawn_children(self):
        if self.length < Decimal('1e-15'):
            return []
        cos = Decimal(4) / 5
        sin = Decimal(3) / 5
        p3x = cos * (cos * (self.p2x - self.p1x) - sin * (self.p2y - self.p1y)) + self.p1x
        p3y = cos * (sin * (self.p2x - self.p1x) + cos * (self.p2y - self.p1y)) + self.p1y
        p4x = self.p1y - p3y + self.p1x
        p4y = p3x - self.p1x + self.p1y
        p5x = p4x + p3x - self.p1x
        p5y = p4y + p3y - self.p1y
        p7x = p3y - self.p2y + self.p2x
        p7y = self.p2x - p3x + self.p2y
        p6x = p7x + p3x - self.p2x
        p6y = p7y + p3y - self.p2y
        left = Square(p4x, p4y, p5x, p5y)
        right = Square(p6x, p6y, p7x, p7y)
        return [left, right]

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 395: find the smallest area of an axis-aligned rectangle enclosing the Pythagorean tree fractal.
    None (prints the area rounded to 10 decimal places).

    Method / Math Rationale
    -----------------------
    Simulate the Pythagorean tree by representing each square by its outer side, updating bounds only from new outer vertices,
    and pruning to retain only squares achieving the level's extremal coordinates in the new points.

    Complexity
    ----------
    O(D * B), where D is the depth (~50), B is the number of boundary squares per level (small constant).

    References
    ----------
    https://projecteuler.net/problem=395
    """
    initial = Square(Decimal(0), Decimal(1), Decimal(1), Decimal(1))
    current = [initial]
    min_x = Decimal(0)
    max_x = Decimal(1)
    min_y = Decimal(0)
    max_y = Decimal(1)
    for _ in tqdm(range(200)):
        new_squares = []
        for sq in current:
            children = sq.spawn_children()
            new_squares.extend(children)
        if not new_squares:
            break

        for sq in new_squares:
            min_x = min(min_x, sq.p1x, sq.p2x)
            max_x = max(max_x, sq.p1x, sq.p2x)
            min_y = min(min_y, sq.p1y, sq.p2y)
            max_y = max(max_y, sq.p1y, sq.p2y)

        retained = []
        eps = Decimal("1e-15")
        for sq in new_squares:
            sq_minx = min(sq.p1x, sq.p2x)
            sq_maxx = max(sq.p1x, sq.p2x)
            sq_miny = min(sq.p1y, sq.p2y)
            sq_maxy = max(sq.p1y, sq.p2y)

            reach = sq.length * Decimal(5)

            could_extend = (
                sq_minx - reach < min_x - eps or
                sq_maxx + reach > max_x + eps or
                sq_miny - reach < min_y - eps or
                sq_maxy + reach > max_y + eps
            )
            if could_extend:
                retained.append(sq)
        current = retained
    area = (max_x - min_x) * (max_y - min_y)
    print(f"{float(area):.10f}")

if __name__ == "__main__":
    main()