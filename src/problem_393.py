# Problem: https://projecteuler.net/problem=393
from functools import lru_cache
from tqdm import tqdm

size = 10

MOVE_UP = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2
MOVE_LEFT = 3

@lru_cache(maxsize=None)
def search(row, down, up):
    if row == size:
        return 2 if down == 0 and up == 0 else 0

    result = 0
    combinations = 1 << (2 * size)
    i = 0
    pbar = tqdm(total=combinations, desc=f"Processing row {row}", position=row, leave=False)
    while i < combinations:
        def get_move(b, p):
            mypos = size - p - 1
            return (b >> (2 * mypos)) & 3

        first_move = get_move(i, 0)
        if first_move == MOVE_LEFT:
            skip_squares = size - 1
            skip_ids = 1 << (2 * skip_squares)
            pbar.update(skip_ids)
            i += skip_ids
            continue

        last_move = get_move(i, size - 1)
        if last_move == MOVE_RIGHT:
            pbar.update(1)
            i += 1
            continue

        if row == 0 and first_move != MOVE_RIGHT:
            pbar.update(1)
            i += 1
            continue

        previous = MOVE_RIGHT
        invalid = False
        failed_at = 0
        for pos in range(size):
            current = get_move(i, pos)
            bit = 1 << pos
            if current == MOVE_UP:
                if (down & bit) != 0:
                    invalid = True
                if (up & bit) == 0:
                    invalid = True
            else:
                if (up & bit) != 0:
                    invalid = True
            if current == MOVE_LEFT and previous == MOVE_RIGHT:
                invalid = True
            if current == MOVE_DOWN and row + 1 == size:
                invalid = True
            if invalid:
                failed_at = pos
                break
            previous = current

        if invalid:
            if failed_at != size - 1:
                skip_squares = size - (failed_at + 1)
                skip_ids = 1 << (2 * skip_squares)
                pbar.update(skip_ids)
                i += skip_ids
            else:
                pbar.update(1)
                i += 1
            continue

        movement = [0] * size
        for pos in range(size):
            bit = 1 << pos
            if down & bit:
                movement[pos] += 1
            movement[pos] -= 1
            current = get_move(i, pos)
            if current == MOVE_LEFT:
                movement[pos - 1] += 1
            elif current == MOVE_RIGHT:
                movement[pos + 1] += 1

        next_down = 0
        next_up = 0
        invalid = False
        for pos in range(size):
            bit = 1 << pos
            current = get_move(i, pos)
            if current == MOVE_DOWN:
                next_down |= bit
            if movement[pos] > 0 or movement[pos] < -1:
                invalid = True
            if movement[pos] == -1:
                next_up |= bit
                if current == MOVE_DOWN:
                    invalid = True

        if invalid:
            pbar.update(1)
            i += 1
            continue

        result += search(row + 1, next_down, next_up)
        pbar.update(1)
        i += 1
    pbar.close()
    return result

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 393: count the number of ways ants on a 10x10 grid can move to
    adjacent squares without ending on the same square or crossing edges.
    No parameters.
    Prints the result.

    Method / Math Rationale
    -----------------------
    Uses dynamic programming to process the grid row by row. State defined by current row and
    masks for incoming downward and required upward moves.
    Each row's possible move combinations are enumerated (4^n), validated for no crossings,
    boundary conditions, and balance of ants per square.
    Memoization on states (row, down_mask, up_mask).
    Symmetry: for first row, force leftmost ant to move right and multiply final valid configs
    by 2.

    Complexity
    ----------
    Time: O(number of states * 4^n), with n=10, 4^10 ~1M per row, 11 rows, but with skips and
    cache, feasible.
    Space: O(number of states) ~ 11 * 2^10 * 2^10 ~ 11M.

    References
    ----------
    https://projecteuler.net/problem=393
    https://euler.stephan-brumme.com/393/
    """
    print(search(0, 0, 0))

if __name__ == "__main__":
    main()