# Problem: https://projecteuler.net/problem=260
import numpy as np
from tqdm import tqdm

def main() -> None:
    """
    Purpose: Solves Project Euler problem 260 by identifying all losing configurations in a three-pile stone game
    where pile sizes are up to 1000 and computing the sum of their pile sizes.

    Args: None

    Returns: None; the computed sum is printed to standard output.

    Method / Math Rationale: Processes potential losing positions (a <= b <= c) in lexicographical order using
    dynamic programming. For each triple, checks if any emptying move—single-pile (to (0, b, c) etc.), two-pile (to
    (0, b-a, c) etc.), or three-pile (to (0, b-a, c-a))—leads to a previously marked losing position via specialized
    arrays. If no such move exists, classifies as losing, adds a + b + c to the sum, and marks the corresponding
    emptying targets in the arrays for future positions. The order ensures move targets are smaller and already
    evaluated, correctly identifying P-positions (losing) as those with no move to another P-position, with emptying
    moves sufficing due to the game's structure as verified by the n=100 sample.

    Complexity: Time O(N^3) for N=1000 with early skips; space O(N^2) for marking arrays.

    References: https://projecteuler.net/problem=260
    Impartial game theory and P-positions.
    """
    max_pile_size = 1000
    size = max_pile_size + 1
    losing_pairs = np.zeros((size, size), dtype=np.int8)
    losing_two_pile_diffs = np.zeros((size, size), dtype=np.int8)
    losing_three_pile_diffs = np.zeros((size, size), dtype=np.int8)
    total_sum = 0
    for min_pile in tqdm(range(size)):
        for mid_pile in range(min_pile, size):
            if losing_pairs[min_pile, mid_pile] == 1:
                continue
            for max_pile in range(mid_pile, size):
                if (losing_pairs[mid_pile, max_pile] == 1 or
                    losing_pairs[min_pile, max_pile] == 1 or
                    losing_pairs[min_pile, mid_pile] == 1):
                    continue
                diff_mid_min = mid_pile - min_pile
                diff_max_mid = max_pile - mid_pile
                diff_max_min = max_pile - min_pile
                if (losing_two_pile_diffs[diff_mid_min, max_pile] == 1 or
                    losing_two_pile_diffs[diff_max_mid, min_pile] == 1 or
                    losing_two_pile_diffs[diff_max_min, mid_pile] == 1):
                    continue
                if losing_three_pile_diffs[diff_mid_min, diff_max_min] == 1:
                    continue
                total_sum += min_pile + mid_pile + max_pile
                losing_pairs[mid_pile, max_pile] = 1
                losing_pairs[min_pile, max_pile] = 1
                losing_pairs[min_pile, mid_pile] = 1
                losing_two_pile_diffs[diff_mid_min, max_pile] = 1
                losing_two_pile_diffs[diff_max_mid, min_pile] = 1
                losing_two_pile_diffs[diff_max_min, mid_pile] = 1
                losing_three_pile_diffs[diff_mid_min, diff_max_min] = 1
    print(total_sum)

if __name__ == "__main__":
    main()