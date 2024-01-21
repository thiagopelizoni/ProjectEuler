# Problem: https://projecteuler.net/problem=67
import requests

def get_triangle():
    url = 'https://projecteuler.net/resources/documents/0067_triangle.txt'
    response = requests.get(url)

    file_lines = response.text.strip().split('\n')

    triangle = []

    for line in file_lines:
        row = [int(number) for number in line.split()]
        triangle.append(row)

    return triangle

if __name__ == "__main__":
    triangle = get_triangle()

    for row in range(len(triangle) - 2, -1, -1):
        for col in range(len(triangle[row])):
            triangle[row][col] += max(triangle[row + 1][col], triangle[row + 1][col + 1])

    answer = triangle[0][0]
    print(answer)
