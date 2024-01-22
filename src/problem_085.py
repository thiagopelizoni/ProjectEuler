# Problem: https://projecteuler.net/problem=85
TARGET_RECTANGLES = 2_000_000

def rectangles_in_grid(w, h):
    return (w * (w + 1) * h * (h + 1)) // 4

closest_area = 0
closest_difference = float('inf')


limit = int(TARGET_RECTANGLES**0.5) + 1

for w in range(1, limit):
    for h in range(1, limit):
        rectangles = rectangles_in_grid(w, h)
        difference = abs(TARGET_RECTANGLES - rectangles)
        if difference < closest_difference:
            closest_difference = difference
            closest_area = w * h

print(closest_area)
