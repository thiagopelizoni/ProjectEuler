# Problem: https://projecteuler.net/problem=210
import math
from tqdm import tqdm

radius_parameter_r = 1000000000
c_value = radius_parameter_r // 4
squared_radius_q = c_value * c_value // 2

if squared_radius_q > 0:
    maximum_a_value = math.isqrt(squared_radius_q - 1)
    number_of_interior_points = 0
    for current_a in tqdm(range(maximum_a_value + 1)):
        current_m = squared_radius_q - current_a * current_a
        current_k = math.isqrt(current_m - 1)
        current_contribution = 2 * current_k + 1
        if current_a == 0:
            number_of_interior_points += current_contribution
        else:
            number_of_interior_points += 2 * current_contribution
else:
    number_of_interior_points = 0

three_halves_r_squared = 3 * radius_parameter_r * radius_parameter_r // 2
result_n = three_halves_r_squared + number_of_interior_points - c_value + 1
print(result_n)