# Problem: https://projecteuler.net/problem=188
import sys
from tqdm import tqdm

def compute_euler_totient(n):
    if n <= 1:
        return 1
    count_two = 0
    temp_n = n
    while temp_n % 2 == 0:
        count_two += 1
        temp_n //= 2
    count_five = 0
    while temp_n % 5 == 0:
        count_five += 1
        temp_n //= 5
    if temp_n != 1:
        print("Error: modulus not power of 2 and 5")
        sys.exit(1)
    if count_five == 0:
        return 2 ** (count_two - 1)
    elif count_two == 0:
        return 4 * (5 ** (count_five - 1))
    else:
        return 2 ** (count_two - 1) * 4 * (5 ** (count_five - 1))

base_number = 1777
tetration_height = 1855
modulus = 100000000

phi_chain_list = []
current_modulus = modulus
while current_modulus >= 1:
    phi_chain_list.append(current_modulus)
    if current_modulus == 1:
        break
    current_modulus = compute_euler_totient(current_modulus)

effective_reduction_depth = min(tetration_height - 1, len(phi_chain_list) - 1)
initial_mod_index = effective_reduction_depth
current_result = base_number % phi_chain_list[initial_mod_index]

progress_range = range(initial_mod_index - 1, -1, -1)
for current_index in tqdm(progress_range, desc="Computing tetration levels"):
    current_result = pow(base_number, current_result, phi_chain_list[current_index])

print(current_result)