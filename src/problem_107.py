# Problem: https://projecteuler.net/problem=107
import requests
import numpy as np

def parse_network(data):
    lines = data.strip().split('\n')
    size = len(lines)
    matrix = np.zeros((size, size), dtype=int)
    for i, line in enumerate(lines):
        values = line.split(',')
        for j, value in enumerate(values):
            if value != '-':
                matrix[i, j] = int(value)
    return matrix

def prim_mst(matrix):
    size = len(matrix)
    selected = [False] * size
    selected[0] = True
    edges = 0
    total_weight = 0
    while edges < size - 1:
        minimum = float('inf')
        x = 0
        y = 0
        for i in range(size):
            if selected[i]:
                for j in range(size):
                    if not selected[j] and matrix[i, j]:
                        if minimum > matrix[i, j]:
                            minimum = matrix[i, j]
                            x = i
                            y = j
        total_weight += matrix[x, y]
        selected[y] = True
        edges += 1
    return total_weight

if __name__ == "__main__":
    url = "https://projecteuler.net/resources/documents/0107_network.txt"
    response = requests.get(url)
    data = response.text

    network_matrix = parse_network(data)
    initial_weight = np.sum(network_matrix) // 2
    mst_weight = prim_mst(network_matrix)
    savings = initial_weight - mst_weight

    print(savings)
