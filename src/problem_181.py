# Problem: https://projecteuler.net/problem=181
from tqdm import tqdm

number_of_black_pebbles = 60
number_of_white_pebbles = 40

ways_to_group = [[0] * (number_of_white_pebbles + 1) for _ in range(number_of_black_pebbles + 1)]
ways_to_group[0][0] = 1

for black_in_current_group in tqdm(range(number_of_black_pebbles + 1)):
    for white_in_current_group in range(number_of_white_pebbles + 1):
        if black_in_current_group + white_in_current_group == 0:
            continue
        for current_total_black in range(black_in_current_group, number_of_black_pebbles + 1):
            for current_total_white in range(white_in_current_group, number_of_white_pebbles + 1):
                ways_to_group[current_total_black][current_total_white] += ways_to_group[current_total_black - black_in_current_group][current_total_white - white_in_current_group]

print(ways_to_group[number_of_black_pebbles][number_of_white_pebbles])