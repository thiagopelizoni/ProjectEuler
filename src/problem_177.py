# Problem: https://projecteuler.net/problem=177
import math
from bisect import bisect_left, bisect_right
from tqdm import tqdm

sin_values = [0.0] * 181
for degree in range(1, 181):
    sin_values[degree] = math.sin(math.radians(degree))

unique_quadrilaterals = set()
small_tolerance = 1e-12

for diagonal_p in tqdm(range(2, 179)):
    diagonal_q = 180 - diagonal_p
    left_configurations = []
    for angle_alpha in range(1, diagonal_p):
        angle_beta = diagonal_p - angle_alpha
        for angle_gamma in range(1, diagonal_q):
            angle_delta = diagonal_q - angle_gamma
            current_ratio = (sin_values[angle_beta] * sin_values[angle_delta]) / (sin_values[angle_alpha] * sin_values[angle_gamma])
            left_configurations.append((current_ratio, angle_alpha, angle_gamma))
    left_configurations.sort(key=lambda config: config[0])
    right_configurations = []
    for angle_epsilon in range(1, diagonal_p):
        angle_zeta = diagonal_p - angle_epsilon
        for angle_theta in range(1, diagonal_q):
            angle_eta = diagonal_q - angle_theta
            current_ratio = (sin_values[angle_epsilon] * sin_values[angle_eta]) / (sin_values[angle_zeta] * sin_values[angle_theta])
            right_configurations.append((current_ratio, angle_epsilon, angle_theta))
    right_configurations.sort(key=lambda config: config[0])
    for left_index in range(len(left_configurations)):
        left_ratio, angle_alpha, angle_gamma = left_configurations[left_index]
        lower_index = bisect_left(right_configurations, left_ratio - small_tolerance, key=lambda config: config[0])
        upper_index = bisect_right(right_configurations, left_ratio + small_tolerance, key=lambda config: config[0])
        for right_index in range(lower_index, upper_index):
            right_ratio, angle_epsilon, angle_theta = right_configurations[right_index]
            angle_beta = diagonal_p - angle_alpha
            angle_delta = diagonal_q - angle_gamma
            angle_zeta = diagonal_p - angle_epsilon
            angle_eta = diagonal_q - angle_theta
            angle_sequence = [angle_alpha, angle_beta, angle_gamma, angle_delta, angle_epsilon, angle_zeta, angle_eta, angle_theta]
            equivalent_sequences = []
            for shift_amount in [0, 2, 4, 6]:
                shifted_sequence = angle_sequence[shift_amount:] + angle_sequence[:shift_amount]
                equivalent_sequences.append(tuple(shifted_sequence))
            reversed_sequence = list(reversed(angle_sequence))
            for shift_amount in [0, 2, 4, 6]:
                shifted_sequence = reversed_sequence[shift_amount:] + reversed_sequence[:shift_amount]
                equivalent_sequences.append(tuple(shifted_sequence))
            canonical_representation = min(equivalent_sequences)
            unique_quadrilaterals.add(canonical_representation)

print(len(unique_quadrilaterals))