# Problem: https://projecteuler.net/problem=62
from collections import defaultdict

def is_cube(n):
    return round(n ** (1/3)) ** 3 == n

def cube_signature(n):
    return ''.join(sorted(str(n)))

def main():
    cubes_by_signature = defaultdict(list)

    n = 1
    while True:
        cube = n**3
        signature = cube_signature(cube)
        cubes_by_signature[signature].append(cube)

        if len(cubes_by_signature[signature]) == 5:
            smallest_cube = min(cubes_by_signature[signature])
            break

        n += 1
    return smallest_cube

if __name__ == "__main__":
    print(main())
