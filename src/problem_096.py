# Problem: https://projecteuler.net/problem=96
import requests

def parse_sudoku(grid_string):
    return [[int(c) for c in grid_string[i:i+9]] for i in range(0, 81, 9)]

def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def is_valid(grid, row, col, num):
    if any(grid[row][c] == num for c in range(9)):
        return False
    if any(grid[r][col] == num for r in range(9)):
        return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    if any(grid[r][c] == num for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)):
        return False
    return True

def solve_sudoku(grid):
    empty_loc = find_empty_location(grid)
    if not empty_loc:
        return True
    row, col = empty_loc
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def get_sudoku_sum(grids):
    total_sum = 0
    for grid in grids:
        lines = grid.strip().split("\n")[1:]
        grid_string = ''.join(lines)
        sudoku = parse_sudoku(grid_string)
        solve_sudoku(sudoku)
        total_sum += 100 * sudoku[0][0] + 10 * sudoku[0][1] + sudoku[0][2]
    return total_sum

if __name__ == "__main__":
    url = "https://projecteuler.net/project/resources/p096_sudoku.txt"
    response = requests.get(url)
    sudoku_text = response.text

    grids = sudoku_text.strip().split("Grid")
    grids = ["Grid" + grid for grid in grids if grid.strip()]
    result = get_sudoku_sum(grids)
    print(result)
