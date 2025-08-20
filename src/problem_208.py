# Problem: https://projecteuler.net/problem=208
from collections import defaultdict
from tqdm import tqdm

num_arcs = 70
max_per_arc = num_arcs // 5
current_ways_dictionary = defaultdict(int)
current_ways_dictionary[(0, 0, 0, 0, 0, 0)] = 1

for current_step in tqdm(range(num_arcs)):
    next_ways_dictionary = defaultdict(int)
    for current_state, number_of_ways in current_ways_dictionary.items():
        current_direction, count_zero, count_one, count_two, count_three, count_four = current_state
        count_list = [count_zero, count_one, count_two, count_three, count_four]
        for direction_delta in [1, 4]:
            new_direction = (current_direction + direction_delta) % 5
            if count_list[new_direction] < max_per_arc:
                new_count_list = count_list[:]
                new_count_list[new_direction] += 1
                new_state = (new_direction, new_count_list[0], new_count_list[1], new_count_list[2], new_count_list[3], new_count_list[4])
                next_ways_dictionary[new_state] += number_of_ways
    current_ways_dictionary = next_ways_dictionary

final_answer = 0
for final_state, number_of_ways in current_ways_dictionary.items():
    final_direction, count_zero, count_one, count_two, count_three, count_four = final_state
    if final_direction == 0 and count_zero == count_one == count_two == count_three == count_four:
        final_answer += number_of_ways

print(final_answer)