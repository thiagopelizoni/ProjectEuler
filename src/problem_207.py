# Problem: https://projecteuler.net/problem=207
from tqdm import tqdm

number_of_perfect_partitions = 0
number_of_total_partitions = 0
threshold_denominator = 12345
safe_upper_limit_for_x = 1000000

for current_x in tqdm(range(2, safe_upper_limit_for_x)):
    current_k = current_x * (current_x - 1)
    is_perfect_partition = (current_x & (current_x - 1)) == 0

    if is_perfect_partition:
        number_of_perfect_partitions += 1

    number_of_total_partitions += 1
    if number_of_perfect_partitions * threshold_denominator < number_of_total_partitions:
        print(current_k)
        break