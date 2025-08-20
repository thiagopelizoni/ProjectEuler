# Problem: https://projecteuler.net/problem=212
import numpy as np
from tqdm import tqdm

class Cuboid:
    def __init__(self, x0, dx, y0, dy, z0, dz):
        self.x1 = x0
        self.x2 = x0 + dx
        self.y1 = y0
        self.y2 = y0 + dy
        self.z1 = z0
        self.z2 = z0 + dz

class SegmentTree:
    def __init__(self, y_list):
        self.y_list = y_list
        self.n = len(y_list) - 1
        self.min_count = [0] * (4 * self.n)
        self.max_count = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.segment_lengths = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1)

    def build(self, node, start, end):
        if start == end:
            self.segment_lengths[node] = self.y_list[start + 1] - self.y_list[start]
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid)
        self.build(2 * node + 1, mid + 1, end)
        self.segment_lengths[node] = self.segment_lengths[2 * node] + self.segment_lengths[2 * node + 1]

    def push(self, node, start, end):
        self.min_count[node] += self.lazy[node]
        self.max_count[node] += self.lazy[node]
        if start != end:
            self.lazy[2 * node] += self.lazy[node]
            self.lazy[2 * node + 1] += self.lazy[node]
        self.lazy[node] = 0

    def update(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if start > end or start > r or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] += val
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self.update(2 * node, start, mid, l, r, val)
        self.update(2 * node + 1, mid + 1, end, l, r, val)
        self.min_count[node] = min(self.min_count[2 * node], self.min_count[2 * node + 1])
        self.max_count[node] = max(self.max_count[2 * node], self.max_count[2 * node + 1])

    def query_covered(self, node, start, end):
        self.push(node, start, end)
        if self.min_count[node] > 0:
            return self.segment_lengths[node]
        if self.max_count[node] <= 0:
            return 0
        if start == end:
            return self.segment_lengths[node] if self.min_count[node] > 0 else 0
        mid = (start + end) // 2
        left_covered = self.query_covered(2 * node, start, mid)
        right_covered = self.query_covered(2 * node + 1, mid + 1, end)
        return left_covered + right_covered

def compute_union_area(active_cuboids_list):
    if not active_cuboids_list:
        return 0
    unique_y_coordinates_set = set()
    for current_cuboid in active_cuboids_list:
        unique_y_coordinates_set.add(current_cuboid.y1)
        unique_y_coordinates_set.add(current_cuboid.y2)
    sorted_y_list = sorted(unique_y_coordinates_set)
    if len(sorted_y_list) < 2:
        return 0
    y_to_index_dictionary = {y_value: index for index, y_value in enumerate(sorted_y_list)}
    current_segment_tree = SegmentTree(sorted_y_list)
    x_events_list = []
    for current_cuboid in active_cuboids_list:
        x_events_list.append((current_cuboid.x1, 1, current_cuboid.y1, current_cuboid.y2))
        x_events_list.append((current_cuboid.x2, -1, current_cuboid.y1, current_cuboid.y2))
    x_events_list.sort(key=lambda event_tuple: (event_tuple[0], -event_tuple[1]))
    accumulated_union_area = 0
    previous_x_coordinate = x_events_list[0][0]
    for current_event in x_events_list:
        current_x, event_delta, y_start, y_end = current_event
        x_difference = current_x - previous_x_coordinate
        if x_difference > 0:
            accumulated_union_area += x_difference * current_segment_tree.query_covered(1, 0, current_segment_tree.n - 1)
        left_index = y_to_index_dictionary[y_start]
        right_index = y_to_index_dictionary[y_end] - 1
        if right_index >= left_index:
            current_segment_tree.update(1, 0, current_segment_tree.n - 1, left_index, right_index, event_delta)
        previous_x_coordinate = current_x
    return accumulated_union_area

sequence_array_s = np.zeros(300001, dtype=np.int64)
for current_k in range(1, 56):
    sequence_array_s[current_k] = (100003 - 200003 * current_k + 300007 * current_k**3) % 1000000
for current_k in range(56, 300001):
    sequence_array_s[current_k] = (sequence_array_s[current_k - 24] + sequence_array_s[current_k - 55]) % 1000000

all_cuboids_list = []
for cuboid_index_n in range(1, 50001):
    base_index = 6 * cuboid_index_n - 5
    x_start = sequence_array_s[base_index] % 10000
    y_start = sequence_array_s[base_index + 1] % 10000
    z_start = sequence_array_s[base_index + 2] % 10000
    dx_length = 1 + sequence_array_s[base_index + 3] % 399
    dy_length = 1 + sequence_array_s[base_index + 4] % 399
    dz_length = 1 + sequence_array_s[base_index + 5] % 399
    all_cuboids_list.append(Cuboid(x_start, dx_length, y_start, dy_length, z_start, dz_length))

z_events_list = []
for current_cuboid_object in all_cuboids_list:
    z_events_list.append((current_cuboid_object.z1, 1, current_cuboid_object))
    z_events_list.append((current_cuboid_object.z2, -1, current_cuboid_object))
z_events_list.sort(key=lambda event_tuple: (event_tuple[0], -event_tuple[1]))

active_cuboids_set = set()
previous_z_coordinate = z_events_list[0][0]
accumulated_total_volume = 0
for current_event in tqdm(z_events_list):
    current_z_coordinate, event_type_delta, current_cuboid_object = current_event
    if current_z_coordinate > previous_z_coordinate:
        current_union_area_value = compute_union_area(list(active_cuboids_set))
        accumulated_total_volume += (current_z_coordinate - previous_z_coordinate) * current_union_area_value
    if event_type_delta == 1:
        active_cuboids_set.add(current_cuboid_object)
    else:
        active_cuboids_set.remove(current_cuboid_object)
    previous_z_coordinate = current_z_coordinate

print(accumulated_total_volume)