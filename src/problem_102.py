# Problem: https://projecteuler.net/problem=102
import requests

def get_triangles():
    url = "https://projecteuler.net/resources/documents/0102_triangles.txt"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

    file_data = response.text

    return [data.split(",") for data in file_data.split("\n")]

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def point_in_triangle(pt, v1, v2, v3):
    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0
    return ((b1 == b2) and (b2 == b3))

def check_triangle_contains_origin(triangle):
    if not len(triangle) == 6 and all(coord.isdigit() or not (coord.startswith('-') and coord[1:].isdigit()) for coord in triangle):
        return False

    A = (int(triangle[0]), int(triangle[1]))
    B = (int(triangle[2]), int(triangle[3]))
    C = (int(triangle[4]), int(triangle[5]))
    origin = (0, 0)
    return point_in_triangle(origin, A, B, C)

triangles = get_triangles()
# Count the number of triangles that contain the origin using the new data structure
count = sum(check_triangle_contains_origin(triangle) for triangle in triangles if triangle != [''])

print(count)
