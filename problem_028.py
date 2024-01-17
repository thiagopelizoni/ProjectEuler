# Problem: https://projecteuler.net/problem=28

def spiral_diagonals_sum(size):
    total = 1
    current_number = 1

    for layer in range(1, size // 2 + 1):
        step = 2 * layer
        for _ in range(4):
            current_number += step
            total += current_number

    return total

if __name__ == "__main__":
    answer = spiral_diagonals_sum(1001)
    print(answer)
