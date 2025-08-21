# Problem: https://projecteuler.net/problem=224
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
from sympy.ntheory.residue_ntheory import sqrt_mod

def process_side_difference(side_difference):
    if side_difference % 2 == 0:
        return 0
    local_count = 0
    modulus = 2 * side_difference
    power_of_two = 2
    odd_part_modulus = side_difference
    solutions_power_of_two = [1]
    if odd_part_modulus == 1:
        solutions_v = solutions_power_of_two
    else:
        solutions_odd_part = sqrt_mod(-1, odd_part_modulus, all_roots=True)
        if not solutions_odd_part:
            return 0
        solutions_v = []
        for solution_a in solutions_power_of_two:
            for solution_b in solutions_odd_part:
                inverse = pow(power_of_two, -1, odd_part_modulus)
                difference = (solution_b - solution_a) % odd_part_modulus
                step = difference * inverse % odd_part_modulus
                v_value = solution_a + power_of_two * step
                solutions_v.append(v_value)
    possible_remainders = [(v + side_difference) % modulus for v in solutions_v]
    for remainder in possible_remainders:
        side_a = remainder
        if side_a < side_difference + 1:
            diff_to_next = side_difference + 1 - side_a
            steps = (diff_to_next + modulus - 1) // modulus
            side_a += steps * modulus
        while True:
            if side_a == 0:
                side_a += modulus
                continue
            squared_a_plus_one = side_a ** 2 + 1
            if squared_a_plus_one % side_difference != 0:
                side_a += modulus
                continue
            side_sum_e = squared_a_plus_one // side_difference
            if side_sum_e <= side_difference:
                break
            side_b = (side_sum_e - side_difference) // 2
            perimeter = side_a + side_sum_e
            if perimeter > perimeter_limit:
                break
            if side_b >= side_a:
                local_count += 1
            side_a += modulus
    return local_count

if __name__ == '__main__':
    perimeter_limit = 75_000_000
    maximum_side_difference = perimeter_limit // 4
    total_barely_obtuse_triangles = 0
    odd_side_differences = list(range(1, maximum_side_difference + 1, 2))
    number_of_processes = multiprocessing.cpu_count()
    with Pool(number_of_processes) as pool:
        chunk_size = max(1, len(odd_side_differences) // (number_of_processes * 100))
        results = list(tqdm(pool.imap(process_side_difference, odd_side_differences, chunksize=chunk_size), total=len(odd_side_differences)))
    total_barely_obtuse_triangles = sum(results)
    print(total_barely_obtuse_triangles)