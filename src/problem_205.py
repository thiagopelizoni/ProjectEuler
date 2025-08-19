# Problem: https://projecteuler.net/problem=205
import numpy as np
from tqdm import tqdm

def compute_dice_distribution(number_of_dice, number_of_sides):
    single_die_polynomial = np.zeros(number_of_sides + 1, dtype=np.int64)
    single_die_polynomial[1:number_of_sides + 1] = 1
    current_distribution = single_die_polynomial.copy()
    for _ in tqdm(range(1, number_of_dice), desc=f"Convolving {number_of_sides}-sided dice distribution"):
        current_distribution = np.convolve(current_distribution, single_die_polynomial)
    return current_distribution

peter_number_of_dice = 9
peter_number_of_sides = 4
colin_number_of_dice = 6
colin_number_of_sides = 6

peter_distribution = compute_dice_distribution(peter_number_of_dice, peter_number_of_sides)
colin_distribution = compute_dice_distribution(colin_number_of_dice, colin_number_of_sides)

colin_cumulative_sum = np.cumsum(colin_distribution)

total_outcomes_for_peter = peter_number_of_sides ** peter_number_of_dice
total_outcomes_for_colin = colin_number_of_sides ** colin_number_of_dice
total_possible_outcomes = total_outcomes_for_peter * total_outcomes_for_colin

favorable_outcomes_count = 0
minimum_peter_sum = peter_number_of_dice * 1
maximum_peter_sum = peter_number_of_dice * peter_number_of_sides

for current_peter_sum in range(minimum_peter_sum, maximum_peter_sum + 1):
    ways_for_this_peter_sum = peter_distribution[current_peter_sum]
    if current_peter_sum - 1 >= 0:
        ways_colin_has_lower_sum = colin_cumulative_sum[current_peter_sum - 1]
    else:
        ways_colin_has_lower_sum = 0
    favorable_outcomes_count += ways_for_this_peter_sum * ways_colin_has_lower_sum

probability_peter_wins = favorable_outcomes_count / total_possible_outcomes
print(round(probability_peter_wins, 7))