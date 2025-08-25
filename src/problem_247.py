# Problem: https://projecteuler.net/problem=247
from decimal import Decimal, getcontext
getcontext().prec = 100
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
import heapq
from tqdm import tqdm

def compute_s(x, y):
    discriminant = (x - y) ** 2 + Decimal(4)
    sqrt_discriminant = discriminant.sqrt()
    return (sqrt_discriminant - (x + y)) / Decimal(2)

def compute_side_for_sequence(sequence):
    x_position = Decimal('1')
    y_position = Decimal('0')
    for move in sequence:
        side_length = compute_s(x_position, y_position)
        if move == 'R':
            x_position += side_length
        else:
            y_position += side_length
    return compute_s(x_position, y_position)

all_sequences = []
for positions in combinations(range(6), 3):
    sequence = ['A'] * 6
    for position in positions:
        sequence[position] = 'R'
    all_sequences.append(sequence)

with ProcessPoolExecutor() as executor:
    side_lengths = executor.map(compute_side_for_sequence, all_sequences)

min_side_length = min(side_lengths)

class Region:
    def __init__(self, x_position, y_position, left_count, below_count):
        self.x_position = x_position
        self.y_position = y_position
        self.left_count = left_count
        self.below_count = below_count
        self.side_length = compute_s(x_position, y_position)

def solve_problem():
    index_left = 3
    index_below = 3
    priority_queue = []
    unique_counter = 0
    heap_push = heapq.heappush
    heap_pop = heapq.heappop
    initial_region = Region(Decimal('1'), Decimal('0'), 0, 0)
    heap_push(priority_queue, (-initial_region.side_length, unique_counter, initial_region))
    unique_counter += 1
    candidates_count = 1
    placed_squares_count = 0
    progress_bar = tqdm(desc="Processing squares")
    while candidates_count > 0:
        placed_squares_count += 1
        progress_bar.update(1)
        _, _, current_region = heap_pop(priority_queue)
        above_region = Region(current_region.x_position, current_region.y_position + current_region.side_length, current_region.left_count, current_region.below_count + 1)
        if above_region.side_length > 0:
            heap_push(priority_queue, (-above_region.side_length, unique_counter, above_region))
            unique_counter += 1
            if above_region.left_count <= index_left and above_region.below_count <= index_below:
                candidates_count += 1
        right_region = Region(current_region.x_position + current_region.side_length, current_region.y_position, current_region.left_count + 1, current_region.below_count)
        if right_region.side_length > 0:
            heap_push(priority_queue, (-right_region.side_length, unique_counter, right_region))
            unique_counter += 1
            if right_region.left_count <= index_left and right_region.below_count <= index_below:
                candidates_count += 1
        if current_region.left_count <= index_left and current_region.below_count <= index_below:
            candidates_count -= 1
    progress_bar.close()
    print(placed_squares_count)

solve_problem()