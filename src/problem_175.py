# Problem: https://projecteuler.net/problem=175
import math
from fractions import Fraction
from tqdm import tqdm

def add_bits(run_lengths, count, bit_type):
    if count == 0:
        return
    current_length = len(run_lengths)
    last_bit_type = current_length % 2
    if bit_type == last_bit_type:
        run_lengths[-1] += count
    else:
        run_lengths.append(count)

def compute_run_lengths(run_lengths, current_ratio, progress_bar):
    progress_bar.update(1)
    if current_ratio.denominator == 1:
        add_bits(run_lengths, int(current_ratio) - 1, 0)
        return
    if current_ratio < 1:
        new_ratio = current_ratio / (1 - current_ratio)
        compute_run_lengths(run_lengths, new_ratio, progress_bar)
        add_bits(run_lengths, 1, 1)
        return
    integer_part = current_ratio.numerator // current_ratio.denominator
    fractional_part = current_ratio - integer_part
    compute_run_lengths(run_lengths, fractional_part, progress_bar)
    add_bits(run_lengths, integer_part, 0)

run_lengths_list = [1]
fraction_ratio = Fraction(123456789, 987654321)
loop_iterations_estimate = 100
progress_bar = tqdm(total=loop_iterations_estimate, desc="Computing run lengths")
compute_run_lengths(run_lengths_list, fraction_ratio, progress_bar)
if progress_bar.n > loop_iterations_estimate:
    progress_bar.total = progress_bar.n
progress_bar.close()
shortened_expansion = ','.join(map(str, run_lengths_list))
print(shortened_expansion)