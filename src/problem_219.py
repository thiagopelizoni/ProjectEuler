# Problem: https://projecteuler.net/problem=219
from tqdm import tqdm

target_split_count = 1_000_000_000

splits_per_cost_level = []
total_splits_so_far = 0

splits_per_cost_level.append(1)
total_splits_so_far += 1

progress_bar = tqdm(total=target_split_count - 1, desc="Building sequence")

while total_splits_so_far < target_split_count - 1:
    current_level_index = len(splits_per_cost_level)
    previous_level_splits = splits_per_cost_level[-1]
    splits_four_levels_back = splits_per_cost_level[current_level_index - 4] if current_level_index >= 4 else 0
    new_splits = previous_level_splits + splits_four_levels_back
    splits_per_cost_level.append(new_splits)
    previous_total_splits = total_splits_so_far
    total_splits_so_far += new_splits
    progress_bar.update(total_splits_so_far - previous_total_splits)

progress_bar.close()

cumulative_splits_per_level = []
current_cumulative = 0

for splits in splits_per_cost_level:
    current_cumulative += splits
    cumulative_splits_per_level.append(current_cumulative)

required_splits = target_split_count - 1
last_level_with_required_splits = 0

for level_index in range(len(cumulative_splits_per_level)):
    if cumulative_splits_per_level[level_index] >= required_splits:
        last_level_with_required_splits = level_index
        break

total_cost = 0

if last_level_with_required_splits > 0:
    previous_cumulative_splits = cumulative_splits_per_level[last_level_with_required_splits - 1]
else:
    previous_cumulative_splits = 0

for level_index in range(last_level_with_required_splits):
    total_cost += splits_per_cost_level[level_index] * (level_index + 5)

remaining_splits_needed = required_splits - previous_cumulative_splits
total_cost += remaining_splits_needed * (last_level_with_required_splits + 5)

print(total_cost)