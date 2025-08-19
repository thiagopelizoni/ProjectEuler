# Problem: https://projecteuler.net/problem=197
import decimal
from decimal import Decimal, getcontext
from tqdm import tqdm

getcontext().prec = 50
natural_log_of_two = getcontext().ln(Decimal(2))

def compute_next_term(current_value):
    constant_value = Decimal('30.403243784')
    exponent_value = constant_value - current_value * current_value
    power_of_two = getcontext().exp(exponent_value * natural_log_of_two)
    floored_power = int(power_of_two)
    next_value = Decimal(floored_power) * Decimal('1e-9')
    return next_value

if __name__ == '__main__':
    current_value = Decimal('-1')
    seen_values_dictionary = {}
    sequence_values_list = []
    current_step = 0
    maximum_steps = 10000
    progress_bar = tqdm(total=maximum_steps, desc="Computing sequence")
    while current_step < maximum_steps:
        value_key = str(current_value)
        if value_key in seen_values_dictionary:
            cycle_start_step = seen_values_dictionary[value_key]
            break
        seen_values_dictionary[value_key] = current_step
        sequence_values_list.append(current_value)
        current_value = compute_next_term(current_value)
        current_step += 1
        progress_bar.update(1)
    progress_bar.close()
    u_in_cycle = sequence_values_list[cycle_start_step]
    u_next_in_cycle = sequence_values_list[cycle_start_step + 1]
    sum_of_pair = u_in_cycle + u_next_in_cycle
    formatted_sum = sum_of_pair.quantize(Decimal('0.000000001'))
    print(formatted_sum)