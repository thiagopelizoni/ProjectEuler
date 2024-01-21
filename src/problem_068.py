# Problem: https://projecteuler.net/problem=68
from itertools import permutations

def magic_5_gon_ring():
    inner_perms = permutations(range(1, 6))
    max_string = 0

    for inner in inner_perms:
        total = 10 + sum(inner[:2])

        outer = []
        for i in range(5):
            outer_value = total - inner[i] - inner[(i + 1) % 5]

            if outer_value < 6 or outer_value > 10 or outer_value in outer:
                break
            outer.append(outer_value)

        if len(outer) == 5:
            start_index = outer.index(min(outer))

            string = ""
            for i in range(5):
                index = (start_index + i) % 5
                string += str(outer[index]) + str(inner[index]) + str(inner[(index + 1) % 5])

            if len(string) == 16 and int(string) > max_string:
                max_string = int(string)

    return str(max_string)

if __name__ == "__main__":
    print(magic_5_gon_ring())
