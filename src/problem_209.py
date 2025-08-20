# Problem: https://projecteuler.net/problem=209
from tqdm import tqdm

def compute_next_state(current_state):
    bit_a = (current_state >> 5) & 1
    bit_b = (current_state >> 4) & 1
    bit_c = (current_state >> 3) & 1
    bit_d = (current_state >> 2) & 1
    bit_e = (current_state >> 1) & 1
    bit_f = current_state & 1
    new_bit = bit_a ^ (bit_b & bit_c)
    next_state_value = (bit_b << 5) | (bit_c << 4) | (bit_d << 3) | (bit_e << 2) | (bit_f << 1) | new_bit
    return next_state_value

def compute_lucas_number(length):
    if length == 0:
        return 2
    if length == 1:
        return 1
    prev_prev = 2
    prev = 1
    for num in range(2, length + 1):
        current_value = prev + prev_prev
        prev_prev = prev
        prev = current_value
    return prev

visited = [False] * 64
cycle_lengths = []

for start in tqdm(range(64)):
    if not visited[start]:
        current = start
        cycle_len = 0
        while not visited[current]:
            visited[current] = True
            current = compute_next_state(current)
            cycle_len += 1
        cycle_lengths.append(cycle_len)

result = 1
for cl in cycle_lengths:
    result *= compute_lucas_number(cl)

print(result)