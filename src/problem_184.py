# Problem: https://projecteuler.net/problem=184
import math
import multiprocessing as mp
from tqdm import tqdm
from collections import defaultdict
import bisect

radius = 105
radius_squared = radius * radius

ray_point_counts_dict = defaultdict(int)

for coordinate_x in range(-radius + 1, radius):
    for coordinate_y in range(-radius + 1, radius):
        if coordinate_x * coordinate_x + coordinate_y * coordinate_y < radius_squared and (coordinate_x != 0 or coordinate_y != 0):
            greatest_common_divisor = math.gcd(abs(coordinate_x), abs(coordinate_y))
            reduced_x = coordinate_x // greatest_common_divisor
            reduced_y = coordinate_y // greatest_common_divisor
            ray_point_counts_dict[(reduced_x, reduced_y)] += 1

rays_list = []
for reduced, point_count in ray_point_counts_dict.items():
    angle = math.atan2(reduced[1], reduced[0])
    if angle < 0:
        angle += 2 * math.pi
    rays_list.append((angle, point_count, reduced))

rays_list.sort(key=lambda item: item[0])

number_of_rays = len(rays_list)
ray_angles = [item[0] for item in rays_list]
ray_point_counts = [item[1] for item in rays_list]
ray_reduced = [item[2] for item in rays_list]

prefix_sums = [0] * (number_of_rays + 1)
for index in range(number_of_rays):
    prefix_sums[index + 1] = prefix_sums[index] + ray_point_counts[index]

def compute_partial_sum(start_p, end_p):
    partial_total = 0
    for current_p in tqdm(range(start_p, end_p)):
        reduced_p = ray_reduced[current_p]
        opposite_reduced = (-reduced_p[0], -reduced_p[1])
        target = math.atan2(opposite_reduced[1], opposite_reduced[0])
        if target < 0:
            target += 2 * math.pi
        first_s_index = bisect.bisect_right(ray_angles, target, lo=current_p + 1)
        right_max_index = bisect.bisect_left(ray_angles, target, lo=current_p + 1) - 1
        if first_s_index >= number_of_rays or right_max_index < current_p + 1:
            continue
        left_pointer = current_p + 1
        for current_s in range(first_s_index, number_of_rays):
            reduced_s = ray_reduced[current_s]
            opposite_reduced_s = (-reduced_s[0], -reduced_s[1])
            target_left = math.atan2(opposite_reduced_s[1], opposite_reduced_s[0])
            if target_left < 0:
                target_left += 2 * math.pi
            while left_pointer < current_s and ray_angles[left_pointer] <= target_left:
                left_pointer += 1
            current_right = min(current_s - 1, right_max_index)
            if left_pointer <= current_right:
                sum_of_counts_for_j = prefix_sums[current_right + 1] - prefix_sums[left_pointer]
                partial_total += ray_point_counts[current_p] * sum_of_counts_for_j * ray_point_counts[current_s]
    return partial_total

if __name__ == "__main__":
    number_of_cores = mp.cpu_count()
    chunk_size_approximate = number_of_rays // number_of_cores
    range_chunks = []
    start_current = 0
    for core_index in range(number_of_cores):
        end_current = start_current + chunk_size_approximate
        if core_index == number_of_cores - 1:
            end_current = number_of_rays
        range_chunks.append((start_current, end_current))
        start_current = end_current

    with mp.Pool(number_of_cores) as process_pool:
        partial_results = process_pool.starmap(compute_partial_sum, range_chunks)

    final_total = sum(partial_results)
    print(final_total)