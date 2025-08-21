# Problem: https://projecteuler.net/problem=222
from tqdm import tqdm
import math

available_sphere_radii = list(range(30, 49))
total_available_spheres = len(available_sphere_radii)

first_endpoint_radius = 50
second_endpoint_radius = 49

total_possible_subsets = 1 << total_available_spheres
negative_infinity = float('inf')

dynamic_programming_table = [[-negative_infinity] * total_available_spheres for _ in range(total_possible_subsets)]

for sphere_index in range(total_available_spheres):
    single_sphere_bitmask = 1 << sphere_index
    radius_sum_with_first_endpoint = available_sphere_radii[sphere_index] + first_endpoint_radius
    distance_saving_for_first_pair = radius_sum_with_first_endpoint - 10 * math.sqrt(2 * radius_sum_with_first_endpoint - 100)
    dynamic_programming_table[single_sphere_bitmask][sphere_index] = distance_saving_for_first_pair

complete_subset_bitmask = (1 << total_available_spheres) - 1

for current_subset_bitmask in tqdm(range(total_possible_subsets)):
    for last_sphere_index in range(total_available_spheres):
        
        if (current_subset_bitmask & (1 << last_sphere_index)) == 0:
            continue
            
        current_total_saving = dynamic_programming_table[current_subset_bitmask][last_sphere_index]
        
        if current_total_saving == -negative_infinity:
            continue
            
        for next_sphere_index in range(total_available_spheres):
            
            if (current_subset_bitmask & (1 << next_sphere_index)) != 0:
                continue
                
            new_subset_bitmask = current_subset_bitmask | (1 << next_sphere_index)
            radius_sum_between_spheres = available_sphere_radii[last_sphere_index] + available_sphere_radii[next_sphere_index]
            distance_saving_for_new_pair = radius_sum_between_spheres - 10 * math.sqrt(2 * radius_sum_between_spheres - 100)
            
            new_total_saving = current_total_saving + distance_saving_for_new_pair
            
            if new_total_saving > dynamic_programming_table[new_subset_bitmask][next_sphere_index]:
                dynamic_programming_table[new_subset_bitmask][next_sphere_index] = new_total_saving

maximum_possible_saving = -negative_infinity

for final_sphere_index in range(total_available_spheres):
    final_accumulated_saving = dynamic_programming_table[complete_subset_bitmask][final_sphere_index]
    
    if final_accumulated_saving == -negative_infinity:
        continue
        
    radius_sum_with_second_endpoint = available_sphere_radii[final_sphere_index] + second_endpoint_radius
    distance_saving_for_final_pair = radius_sum_with_second_endpoint - 10 * math.sqrt(2 * radius_sum_with_second_endpoint - 100)
    
    total_saving_for_complete_path = final_accumulated_saving + distance_saving_for_final_pair
    
    if total_saving_for_complete_path > maximum_possible_saving:
        maximum_possible_saving = total_saving_for_complete_path

sum_of_all_radii_doubled = 1680
minimum_pipe_length_millimeters = sum_of_all_radii_doubled - maximum_possible_saving
minimum_pipe_length_micrometers = round(minimum_pipe_length_millimeters * 1000)

print(minimum_pipe_length_micrometers)