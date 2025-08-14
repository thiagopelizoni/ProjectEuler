# Problem: https://projecteuler.net/problem=169
from tqdm import tqdm

big_number = 10 ** 25

subproblem_numbers = set()

def gather_subproblems(num):
    if num <= 0 or num in subproblem_numbers:
        return
    subproblem_numbers.add(num)
    half_num = num // 2
    if num % 2 == 1:
        gather_subproblems(half_num)
    else:
        gather_subproblems(half_num)
        half_minus = half_num - 1
        if half_minus >= 0:
            gather_subproblems(half_minus)

gather_subproblems(big_number)

sorted_subproblems = sorted(subproblem_numbers)

ways_to_make = {0: 1}

for current_num in tqdm(sorted_subproblems):
    half_num = current_num // 2
    if current_num % 2 == 1:
        current_ways = ways_to_make[half_num]
    else:
        current_ways = ways_to_make[half_num]
        half_minus = half_num - 1
        if half_minus >= 0:
            current_ways += ways_to_make[half_minus]
    ways_to_make[current_num] = current_ways

print(ways_to_make[big_number])