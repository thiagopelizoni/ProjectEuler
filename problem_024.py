# Problem: https://projecteuler.net/problem=24
import itertools

millionth = 1000000

def main():
    permutations = itertools.permutations(range(10))

    sorted_permutations = sorted(permutations)

    millionth_permutation = sorted_permutations[millionth - 1]

    answer = ''.join(map(str, millionth_permutation))

    print(answer)


if __name__ == "__main__":
    main()
