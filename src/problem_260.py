# Problem: https://projecteuler.net/problem=260
import numpy as np
from tqdm import tqdm

maximum_pile_size = 1000
size = maximum_pile_size + 1

pair_marked = np.zeros((size, size), dtype=np.int8)
difference_marked = np.zeros((size, size), dtype=np.int8)
all_differences_marked = np.zeros((size, size), dtype=np.int8)

total_sum_of_piles = 0

for pile_a in tqdm(range(size)):
    for pile_b in range(pile_a, size):
        if pair_marked[pile_a, pile_b] == 1:
            continue

        for pile_c in range(pile_b, size):
            if (pair_marked[pile_b, pile_c] == 1 or
                pair_marked[pile_a, pile_c] == 1 or
                pair_marked[pile_a, pile_b] == 1):
                continue

            difference_b_a = pile_b - pile_a
            difference_c_b = pile_c - pile_b
            difference_c_a = pile_c - pile_a

            if (difference_marked[difference_b_a, pile_c] == 1 or
                difference_marked[difference_c_b, pile_a] == 1 or
                difference_marked[difference_c_a, pile_b] == 1):
                continue

            if all_differences_marked[difference_b_a, difference_c_a] == 1:
                continue

            total_sum_of_piles += pile_a + pile_b + pile_c

            pair_marked[pile_b, pile_c] = 1
            pair_marked[pile_a, pile_c] = 1
            pair_marked[pile_a, pile_b] = 1

            difference_marked[difference_b_a, pile_c] = 1
            difference_marked[difference_c_b, pile_a] = 1
            difference_marked[difference_c_a, pile_b] = 1

            all_differences_marked[difference_b_a, difference_c_a] = 1

print(total_sum_of_piles)