# Problem: https://projecteuler.net/problem=94
sum_of_perimeters = 0
side = 2  # Starting from the smallest possible side

# The maximum perimeter constraint
max_perimeter = 1_000_000_000

# Define a function to check if a number is a perfect square
def is_perfect_square(n):
    return n == int(n**0.5)**2

# Define a function to calculate the perimeter
def calc_perimeter(a, b):
    return a * 2 + b

# Loop to find almost equilateral triangles
while True:
    # Case 1: The sides are (side, side, side-1)
    # The squared height of the triangle must be a perfect square for the area to be an integer
    # Using Pythagorean theorem: height^2 = side^2 - ((side-1)/2)^2
    height_squared = 4 * side**2 - (side-1)**2
    if is_perfect_square(height_squared):
        perimeter = calc_perimeter(side, side-1)
        if perimeter > max_perimeter:
            break
        sum_of_perimeters += perimeter

    # Case 2: The sides are (side, side, side+1)
    # Using Pythagorean theorem: height^2 = side^2 - ((side+1)/2)^2
    height_squared = 4 * side**2 - (side+1)**2
    if is_perfect_square(height_squared):
        perimeter = calc_perimeter(side, side+1)
        if perimeter > max_perimeter:
            break
        sum_of_perimeters += perimeter

    # Increment the side length for the next iteration
    side += 1

print(sum_of_perimeters)
