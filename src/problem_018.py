# Problem: https://projecteuler.net/problem=15

# Triangle as given in Project Euler Problem 18
triangle = [
    [75],
    [95, 64],
    [17, 47, 82],
    [18, 35, 87, 10],
    [20, 4, 82, 47, 65],
    [19, 1, 23, 75, 3, 34],
    [88, 2, 77, 73, 7, 63, 67],
    [99, 65, 4, 28, 6, 16, 70, 92],
    [41, 41, 26, 56, 83, 40, 80, 70, 33],
    [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
    [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
    [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
    [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
    [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
    [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]
]

def maximum_path_sum(triangle):
    """
    Function to calculate the maximum total from top to bottom of the given triangle.
    """
    # Starting from the second-last row, move upwards in the triangle
    for row in range(len(triangle) - 2, -1, -1):
        for col in range(len(triangle[row])):
            # For each element, add the maximum of the two adjacent numbers from the row below
            triangle[row][col] += max(triangle[row + 1][col], triangle[row + 1][col + 1])

    # The top element of the triangle now contains the maximum total
    return triangle[0][0]

# Calculate the maximum total from top to bottom of the triangle
if __name__ == "__main__":
    answer = maximum_path_sum(triangle)
    print(answer)
