# Problem: https://projecteuler.net/problem=173
import math
from tqdm import tqdm

maximum_number_of_tiles = 1000000
total_number_of_laminae = 0
maximum_thickness = int(math.sqrt(maximum_number_of_tiles / 4)) + 1

for thickness in tqdm(range(1, maximum_thickness + 1)):
    maximum_inner_offset = maximum_number_of_tiles // (4 * thickness)
    if maximum_inner_offset >= thickness + 1:
        number_for_this_thickness = maximum_inner_offset - thickness
        total_number_of_laminae += number_for_this_thickness

print(total_number_of_laminae)