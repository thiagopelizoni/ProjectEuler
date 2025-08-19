# Problem: https://projecteuler.net/problem=199
from mpmath import mp, mpf, sqrt as mp_sqrt
import multiprocessing as multi_proc
from tqdm import tqdm

def calculate_new_curvature(curv1, curv2, curv3):
    discriminant_value = curv1 * curv2 + curv1 * curv3 + curv2 * curv3
    sqrt_discriminant = mp_sqrt(discriminant_value)
    return curv1 + curv2 + curv3 + mpf(2) * sqrt_discriminant

def process_one_gap(gap_tuple):
    curv1, curv2, curv3 = gap_tuple
    new_curv = calculate_new_curvature(curv1, curv2, curv3)
    radius_squared = mpf(1) / (new_curv ** 2)
    new_gap1 = (curv1, curv2, new_curv)
    new_gap2 = (curv1, curv3, new_curv)
    new_gap3 = (curv2, curv3, new_curv)
    return radius_squared, [new_gap1, new_gap2, new_gap3]

def compute_uncovered_fraction(max_iterations=10):
    mp.dps = 30
    sqrt_three_value = mp_sqrt(mpf(3))
    large_curvature = mpf(3) - mpf(2) * sqrt_three_value
    initial_curvature = mpf(1)
    list_of_gaps = [
        (initial_curvature, initial_curvature, initial_curvature),
        (initial_curvature, initial_curvature, large_curvature),
        (initial_curvature, initial_curvature, large_curvature),
        (initial_curvature, initial_curvature, large_curvature)
    ]
    accumulated_radius_squared = mpf(0)
    for iteration_number in range(max_iterations):
        with multi_proc.Pool() as processing_pool:
            processed_results = list(tqdm(processing_pool.imap(process_one_gap, list_of_gaps),
                                          total=len(list_of_gaps),
                                          desc=f"Iteration {iteration_number + 1} progress"))
        accumulated_radius_squared += sum(one_result[0] for one_result in processed_results)
        list_of_gaps = [one_gap for one_result in processed_results for one_gap in one_result[1]]
    initial_radius_squared_sum = mpf(3)
    total_small_circles_radius_squared = initial_radius_squared_sum + accumulated_radius_squared
    large_radius = mpf(1) + mpf(2) / sqrt_three_value
    large_radius_squared = large_radius ** 2
    fraction_uncovered = mpf(1) - total_small_circles_radius_squared / large_radius_squared
    return fraction_uncovered

if __name__ == "__main__":
    result_fraction = compute_uncovered_fraction()
    print(f"{float(result_fraction):.8f}")