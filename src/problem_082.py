# Problem: https://projecteuler.net/problem=82
import requests

def fetch_matrix():
    url = "https://projecteuler.net/resources/documents/0082_matrix.txt"

    response = requests.get(url)
    file_lines = response.text.strip().split('\n')

    matrix = []
    for line in file_lines:
        row = [int(number) for number in line.split(",")]
        matrix.append(row)
    return matrix

def min_path_sum(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Initialize a matrix to store the minimum path sum at each cell
    min_path_sum = [[float('inf')] * num_cols for _ in range(num_rows)]

    # Initialize the first column with the values of the matrix
    for i in range(num_rows):
        min_path_sum[i][0] = matrix[i][0]

    # Compute the minimum path sum for each cell
    for col in range(1, num_cols):
        for row in range(num_rows):
            min_path_sum[row][col] = min_path_sum[row][col - 1] + matrix[row][col]

        # Update the minimum path sum considering the possibility of moving up or down
        for _ in range(num_rows):
            for row in range(1, num_rows):
                min_path_sum[row][col] = min(min_path_sum[row][col], min_path_sum[row - 1][col] + matrix[row][col])
            for row in range(num_rows - 2, -1, -1):
                min_path_sum[row][col] = min(min_path_sum[row][col], min_path_sum[row + 1][col] + matrix[row][col])

    # Find the minimum path sum in the last column
    return min(min_path_sum[row][-1] for row in range(num_rows))


if __name__ == "__main__":
    matrix = fetch_matrix()
    answer = min_path_sum(matrix)
    print(answer)
