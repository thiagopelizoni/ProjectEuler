# Problem: https://projecteuler.net/problem=131
import sympy

def count_prime_cubes(limit):
    count = 0
    n = 1
    while True:
        cube = (n + 1) ** 3 - n ** 3
        if cube > limit:
            break
        if sympy.isprime(cube):
            count += 1
        n += 1
    return count

def main():
    limit = 1000000
    result = count_prime_cubes(limit)
    print(result)

if __name__ == "__main__":
    main()
