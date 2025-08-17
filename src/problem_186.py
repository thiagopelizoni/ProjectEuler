# Problem: https://projecteuler.net/problem=186
import sys
from collections import deque
from itertools import islice
from tqdm import tqdm

NUMBER_OF_SUBSCRIBERS = 1000000
PRIME_MINISTER_ID = 524287
REQUIRED_CONNECTED_SUBSCRIBERS = 990000
MODULO_VALUE = 1000000
LAG_24 = 24
LAG_55 = 55
INITIAL_SEQUENCE_LENGTH = 55

def create_s_sequence_generator():
    sequence_deque = deque(maxlen=INITIAL_SEQUENCE_LENGTH)
    for sequence_index in range(1, INITIAL_SEQUENCE_LENGTH + 1):
        new_value = (100003 - 200003 * sequence_index + 300007 * sequence_index ** 3) % MODULO_VALUE
        sequence_deque.append(new_value)
        yield new_value

    while True:
        new_value = (sequence_deque[-LAG_24] + sequence_deque[-LAG_55]) % MODULO_VALUE
        sequence_deque.append(new_value)
        yield new_value

def find_root(parent_array, subscriber_id):
    if parent_array[subscriber_id] != subscriber_id:
        parent_array[subscriber_id] = find_root(parent_array, parent_array[subscriber_id])

    return parent_array[subscriber_id]

def union_subscribers(parent_array, rank_array, size_array, subscriber_a, subscriber_b):
    root_a = find_root(parent_array, subscriber_a)
    root_b = find_root(parent_array, subscriber_b)
    if root_a == root_b:
        return

    if rank_array[root_a] < rank_array[root_b]:
        parent_array[root_a] = root_b
        size_array[root_b] += size_array[root_a]
    elif rank_array[root_a] > rank_array[root_b]:
        parent_array[root_b] = root_a
        size_array[root_a] += size_array[root_b]
    else:
        parent_array[root_b] = root_a
        size_array[root_a] += size_array[root_b]
        rank_array[root_a] += 1

parent_list = list(range(NUMBER_OF_SUBSCRIBERS))
rank_list = [0] * NUMBER_OF_SUBSCRIBERS
component_size_list = [1] * NUMBER_OF_SUBSCRIBERS

sequence_generator = create_s_sequence_generator()

successful_call_counter = 0
progress_bar = tqdm(desc="Processing calls", unit=" calls")

while True:
    caller_id = next(sequence_generator)
    callee_id = next(sequence_generator)
    if caller_id != callee_id:
        successful_call_counter += 1
        union_subscribers(parent_list, rank_list, component_size_list, caller_id, callee_id)

    progress_bar.update(1)
    prime_minister_root = find_root(parent_list, PRIME_MINISTER_ID)
    if component_size_list[prime_minister_root] >= REQUIRED_CONNECTED_SUBSCRIBERS:
        print(successful_call_counter)
        break

progress_bar.close()