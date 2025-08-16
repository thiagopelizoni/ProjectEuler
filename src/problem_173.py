# Problem: https://projecteuler.net/problem=173
import math
import numpy as np
from tqdm import tqdm

maximum_tiles = 1000000
laminae_counts_per_tile_number = np.zeros(maximum_tiles + 1, dtype=int)
maximum_thickness = int(math.sqrt(maximum_tiles / 4)) + 1

for thickness in tqdm(range(1, maximum_thickness + 1)):
    minimum_inner_plus_thickness = thickness + 1
    maximum_inner_plus_thickness = maximum_tiles // (4 * thickness)
    for inner_plus_thickness in range(minimum_inner_plus_thickness, maximum_inner_plus_thickness + 1):
        tiles_used = 4 * thickness * inner_plus_thickness
        laminae_counts_per_tile_number[tiles_used] += 1

type_counts = [0] * 11
for tile_number in range(1, maximum_tiles + 1):
    lamina_count = laminae_counts_per_tile_number[tile_number]
    if 1 <= lamina_count <= 10:
        type_counts[lamina_count] += 1

total_number = sum(type_counts)
print(total_number)