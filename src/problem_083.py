# Problem: https://projecteuler.net/problem=83
import requests
import numpy as np

def fetch_matrix():
    url = "https://projecteuler.net/resources/documents/0083_matrix.txt"

    response = requests.get(url)
    file_lines = response.text.strip().split('\n')

    matrix = []
    for line in file_lines:
        row = [int(number) for number in line.split(",")]
        matrix.append(row)
    return matrix

def compute_minimal_path_sum(matrix):
    size = len(matrix)

    path_sum = np.full((size, size), np.inf)
    path_sum[0, 0] = matrix[0][0]

    update_made = True
    while update_made:
        update_made = False
        for y in range(size):
            for x in range(size):
                original_path_sum = path_sum[y, x]
                if x > 0:
                    path_sum[y, x] = min(path_sum[y, x], path_sum[y, x - 1] + matrix[y][x])

                if x < size - 1:
                    path_sum[y, x] = min(path_sum[y, x], path_sum[y, x + 1] + matrix[y][x])

                if y > 0:
                    path_sum[y, x] = min(path_sum[y, x], path_sum[y - 1, x] + matrix[y][x])

                if y < size - 1:
                    path_sum[y, x] = min(path_sum[y, x], path_sum[y + 1, x] + matrix[y][x])

                if path_sum[y, x] != original_path_sum:
                    update_made = True

    return int(path_sum[-1, -1])

if __name__ == "__main__":
    matrix = fetch_matrix()
    answer = compute_minimal_path_sum(matrix)
    print(answer)
