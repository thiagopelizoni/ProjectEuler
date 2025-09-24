# Problem: https://projecteuler.net/problem=349
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 349 by simulating Langton's ant and computing
    the number of black squares after 10^18 moves.

    Method / Math Rationale
    -----------------------
    Simulate the ant's movement on an infinite grid (using a set for black
    squares) until the increase in black squares per cycle of 104 steps
    stabilizes over 10 consecutive cycles. Then, extrapolate the number of black
    squares for the remaining cycles to reach 10^18 moves.

    Complexity
    ----------
    O(initial steps) ~ O(10^4), since simulation stops after detecting steady
    state.

    References
    ----------
    https://projecteuler.net/problem=349
    """
    limit = 10**18
    cycle = 104
    remainder = limit % cycle  # 40
    stop_if_same_deltas = 10

    blacks = set()
    x, y = 0, 0
    dir_idx = 0  # 0: North, 1: East, 2: South, 3: West
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    steps = 0
    count = 0
    last = 0
    last_deltas = []

    pbar = tqdm(desc="Simulating ant moves", unit=" steps")

    while steps < limit:
        pos = (x, y)
        is_black = pos in blacks

        if is_black:
            blacks.remove(pos)
            count -= 1
            dir_idx = (dir_idx - 1) % 4
        else:
            blacks.add(pos)
            count += 1
            dir_idx = (dir_idx + 1) % 4

        dx, dy = deltas[dir_idx]
        x += dx
        y += dy

        steps += 1
        pbar.update()

        if steps % cycle == remainder:
            diff = count - last
            last_deltas.append(diff)
            last = count

            if len(last_deltas) >= stop_if_same_deltas:
                recent_deltas = last_deltas[-stop_if_same_deltas:]
                if all(d == recent_deltas[0] for d in recent_deltas):
                    remaining_cycles = (limit - steps) // cycle
                    count += remaining_cycles * diff
                    break

    pbar.close()
    print(count)

if __name__ == "__main__":
    main()