# Problem: https://projecteuler.net/problem=91
def is_right_triangle(x1, y1, x2, y2):
    # from origin to P
    side1 = x1**2 + y1**2
    # from origin to Q
    side2 = x2**2 + y2**2
    # from P to Q
    side3 = (x1 - x2)**2 + (y1 - y2)**2

    # Check if the sum of the squares of the two shorter sides equals the square of the longest side
    return (side1 + side2 == side3) or (side1 + side3 == side2) or (side2 + side3 == side1)

# Initialize counter for right triangles
right_triangle_count = 0
limit = 51
# Generate all possible points P(x1, y1) and Q(x2, y2) within the given range
for x1 in range(limit):
    for y1 in range(limit):
        for x2 in range(limit):
            for y2 in range(limit):
                if (x1, y1) != (x2, y2) and (x1, y1) != (0, 0) and (x2, y2) != (0, 0):
                    if is_right_triangle(x1, y1, x2, y2):
                        right_triangle_count += 1

# Since each triangle is counted twice (once for each ordering of P and Q), divide by 2
right_triangle_count //= 2

print(right_triangle_count)
