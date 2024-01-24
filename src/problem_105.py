# Problem: https://projecteuler.net/problem=105
from itertools import combinations
import requests

def get_sets():
    url = "https://projecteuler.net/resources/documents/0105_sets.txt"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")

    return [list(map(int, data.split(","))) for data in response.text.strip().split("\n")]

def is_special_sum_set(s):
    # Use a set to store the sum of subsets for quick 'in' checks
    all_sums = set()

    # Use a dict to store unique sum and length pairs
    unique_combinations = {}

    # Generate all possible non-empty subsets
    for i in range(1, len(s) + 1):
        for combo in combinations(s, i):
            combo_sum = sum(combo)
             # Rule 1 violation
            if combo_sum in all_sums:
                return False

            all_sums.add(combo_sum)
            # Store only the smallest length for each sum
            if combo_sum not in unique_combinations or i < unique_combinations[combo_sum]:
                unique_combinations[combo_sum] = i

    # Check Rule 2 by comparing the length of subsets with equal sums
    sums = sorted(unique_combinations.keys())
    for i in range(len(sums) - 1):
        # Rule 2 violation
        if unique_combinations[sums[i]] > unique_combinations[sums[i + 1]]:
            return False

    return True

def find_special_sum(sets):
    special_sum_sets = []
    total_sum = 0

    for set_elements in sets:
        if is_special_sum_set(set_elements):
            special_sum_sets.append(set_elements)
            total_sum += sum(set_elements)

    return special_sum_sets, total_sum

sets = get_sets()

special_sum_sets, total_sum = find_special_sum(sets)

print(total_sum)
