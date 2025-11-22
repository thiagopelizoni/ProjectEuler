# Problem: https://projecteuler.net/problem=260
import numpy as np
from tqdm import tqdm

def main() -> None:
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