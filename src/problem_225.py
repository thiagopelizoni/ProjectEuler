# Problem: https://projecteuler.net/problem=225
from tqdm import tqdm

maximum_steps_for_cycle_detection = 30000
target_number_of_non_divisors = 124
current_odd_number = 1
count_of_non_divisors_found = 0
progress_bar = tqdm(total=target_number_of_non_divisors)

while count_of_non_divisors_found < target_number_of_non_divisors:
    current_odd_number += 2
    tribonacci_previous_two = 1
    tribonacci_previous_one = 1
    tribonacci_current = 1
    is_divisor_of_some_tribonacci = False
    for step in range(maximum_steps_for_cycle_detection):
        next_tribonacci = (tribonacci_previous_two + tribonacci_previous_one + tribonacci_current) % current_odd_number
        if next_tribonacci == 0:
            is_divisor_of_some_tribonacci = True
            break
        tribonacci_previous_two = tribonacci_previous_one
        tribonacci_previous_one = tribonacci_current
        tribonacci_current = next_tribonacci
        if tribonacci_previous_two == 1 and tribonacci_previous_one == 1 and tribonacci_current == 1:
            break
    if not is_divisor_of_some_tribonacci:
        count_of_non_divisors_found += 1
        progress_bar.update(1)

progress_bar.close()
print(current_odd_number)