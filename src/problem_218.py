# Problem: https://projecteuler.net/problem=218
import math
import multiprocessing
from tqdm import tqdm
from math import gcd, sqrt

def process_u(current_u_value):
    count_non_divisible = 0

    try:
        max_v_value = int(sqrt(s_max_limit - current_u_value ** 2))
    except ValueError:
        return 0

    for current_v_value in range(1, min(current_u_value, max_v_value + 1)):
        if current_u_value % 2 == current_v_value % 2:
            continue

        if gcd(current_u_value, current_v_value) != 1:
            continue

        odd_leg = current_u_value ** 2 - current_v_value ** 2
        even_leg = 2 * current_u_value * current_v_value

        if odd_leg > even_leg:
            param_m = odd_leg
            param_n = even_leg
        else:
            param_m = even_leg
            param_n = odd_leg

        difference_m_n = param_m - param_n
        sum_m_n = param_m + param_n

        area_value = param_m * param_n * difference_m_n * sum_m_n

        if area_value % 84 != 0:
            count_non_divisible += 1

    return count_non_divisible


if __name__ == '__main__':
    s_max_limit = 10 ** 8
    max_u_value = int(math.sqrt(s_max_limit))
    u_value_list = list(range(2, max_u_value + 1))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results_list = list(tqdm(pool.imap(process_u, u_value_list), total=len(u_value_list)))

    total_non_divisible_count = sum(results_list)
    print(total_non_divisible_count)