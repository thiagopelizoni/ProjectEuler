# Problem: https://projecteuler.net/problem=191
import numpy as np
from tqdm import tqdm

total_number_of_days = 30
maximum_late_days_allowed = 2
maximum_consecutive_absents_allowed = 3

attendance_ways_array = np.zeros(
    (total_number_of_days + 1, maximum_late_days_allowed, maximum_consecutive_absents_allowed),
    dtype=object
)
attendance_ways_array[0][0][0] = 1

for current_day_number in tqdm(range(1, total_number_of_days + 1)):
    for previous_late_count in range(maximum_late_days_allowed):
        for previous_consecutive_absents in range(maximum_consecutive_absents_allowed):
            current_ways = attendance_ways_array[current_day_number - 1][previous_late_count][previous_consecutive_absents]
            if current_ways == 0:
                continue

            # On time choice
            new_late_count = previous_late_count
            new_consecutive_absents = 0
            attendance_ways_array[current_day_number][new_late_count][new_consecutive_absents] += current_ways

            # Absent choice
            new_late_count = previous_late_count
            new_consecutive_absents = previous_consecutive_absents + 1
            if new_consecutive_absents < maximum_consecutive_absents_allowed:
                attendance_ways_array[current_day_number][new_late_count][new_consecutive_absents] += current_ways

            # Late choice
            new_late_count = previous_late_count + 1
            if new_late_count < maximum_late_days_allowed:
                new_consecutive_absents = 0
                attendance_ways_array[current_day_number][new_late_count][new_consecutive_absents] += current_ways

total_prize_strings = 0
for late_count in range(maximum_late_days_allowed):
    for consecutive_absents in range(maximum_consecutive_absents_allowed):
        total_prize_strings += attendance_ways_array[total_number_of_days][late_count][consecutive_absents]

print(total_prize_strings)