# Problem: https://projecteuler.net/problem=81
import requests

def fetch_matrix():
    url = "https://projecteuler.net/resources/documents/0081_matrix.txt"

    response = requests.get(url)
    file_lines = response.text.strip().split('\n')

    matrix = []
    for line in file_lines:
        row = [int(number) for number in line.split(",")]
        matrix.append(row)
    return matrix

def minimal_path_sum(matrix):
    n = len(matrix)
    m = len(matrix[0])

    # Initialize a cost matrix with the same dimensions as the input matrix.
    # The cost matrix will store the minimal path sum to reach each cell.
    cost = [[0 for _ in range(m)] for _ in range(n)]

    # The cost to reach the top-left cell is just the value of that cell.
    cost[0][0] = matrix[0][0]

    # Initialize the first row of the cost matrix.
    for j in range(1, m):
        cost[0][j] = cost[0][j - 1] + matrix[0][j]

    # Initialize the first column of the cost matrix.
    for i in range(1, n):
        cost[i][0] = cost[i - 1][0] + matrix[i][0]

    # Fill in the rest of the cost matrix.
    for i in range(1, n):
        for j in range(1, m):
            # The cost to reach each cell is the value of the cell itself plus
            # the minimum of the cost to reach the cell above or to the left.
            cost[i][j] = matrix[i][j] + min(cost[i - 1][j], cost[i][j - 1])

    # The minimal path sum is the value in the bottom-right cell of the cost matrix.
    return cost[-1][-1]

if __name__ == "__main__":
    matrix = fetch_matrix()
    print(minimal_path_sum(matrix))
