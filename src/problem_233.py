# Problem: https://projecteuler.net/problem=233
import bisect
import itertools
import math
import sys
from tqdm import tqdm
from sympy.ntheory import sieve

L = 10**11
max_prime = 10**7
max_B = max_prime

primes_list = list(sieve.primerange(3, max_prime + 10))
p1 = [p for p in primes_list if p % 4 == 1]
p1.sort()

prefix_p1 = [0]
for p in p1:
    prefix_p1.append(prefix_p1[-1] + p)

def create_smallest_prime_factor(n):
    spf = [0] * (n + 1)
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            for j in range(i * 2, n + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    return spf

spf = create_smallest_prime_factor(max_B)

sum_prefix = [0] * (max_B + 1)
for n in tqdm(range(1, max_B + 1), desc="Identifying numbers with allowed prime factors"):
    temp = n
    is_allowed = True
    while temp > 1:
        p = spf[temp]
        if p != 2 and p % 4 != 3:
            is_allowed = False
            break
        while temp % p == 0:
            temp //= p
    if is_allowed:
        sum_prefix[n] = n

for i in range(1, max_B + 1):
    sum_prefix[i] += sum_prefix[i - 1]

def compute_sum_over_primes_times_prefix(K, start_index, max_B_value, sum_prefix_list, primes_one_mod_four, primes_sum_prefix):
    if K < primes_one_mod_four[start_index] if start_index < len(primes_one_mod_four) else True:
        return 0

    total = 0
    n_primes = len(primes_one_mod_four)
    lower = primes_one_mod_four[start_index]
    upper = min(primes_one_mod_four[-1], K) if primes_one_mod_four else 0
    end_index = bisect.bisect_right(primes_one_mod_four, K)
    current_lower = lower
    while current_lower <= upper:
        b_value = K // current_lower
        current_upper = K // b_value
        current_upper = min(current_upper, upper)
        left_index = bisect.bisect_left(primes_one_mod_four, current_lower, start_index, end_index)
        right_index = bisect.bisect_right(primes_one_mod_four, current_upper, left_index, end_index) - 1
        if left_index > right_index:
            current_lower = current_upper + 1
            continue
        sum_primes_in_range = primes_sum_prefix[right_index + 1] - primes_sum_prefix[left_index]
        su_value = sum_prefix_list[min(b_value, max_B_value)]
        total += sum_primes_in_range * su_value
        current_lower = current_upper + 1
    return total

total_sum_of_n = 0

five_power_ten = 5 ** 10
max_p2_for_two_ten = math.isqrt(L // five_power_ten)
start_index_for_two_ten = bisect.bisect_right(p1, 5)
for index in range(start_index_for_two_ten, len(p1)):
    p2 = p1[index]
    if p2 > max_p2_for_two_ten:
        break
    m1 = five_power_ten * p2 ** 2
    b_value = L // m1
    su_value = sum_prefix[min(b_value, max_B)]
    total_sum_of_n += m1 * su_value

five_power_seven = 5 ** 7
max_p2_for_three_seven = int((L // five_power_seven) ** (1 / 3))
start_index_for_three_seven = bisect.bisect_right(p1, 5)
for index in range(start_index_for_three_seven, len(p1)):
    p2 = p1[index]
    if p2 > max_p2_for_three_seven:
        break
    m1 = five_power_seven * p2 ** 3
    b_value = L // m1
    su_value = sum_prefix[min(b_value, max_B)]
    total_sum_of_n += m1 * su_value

primes_for_other = [13, 17]
five_power_three = 5 ** 3
for p2 in primes_for_other:
    m1 = five_power_three * p2 ** 7
    b_value = L // m1
    su_value = sum_prefix[min(b_value, max_B)]
    total_sum_of_n += m1 * su_value

exp_permutations = list(itertools.permutations([1, 2, 3]))

small_limit = 5000
small_primes_one_mod_four = [p for p in p1 if p <= small_limit]

for perm_index in range(len(exp_permutations)):
    e_p, e_q, e_r = exp_permutations[perm_index]
    for i in range(len(small_primes_one_mod_four)):
        p = small_primes_one_mod_four[i]
        fixed_p = p ** e_p
        if fixed_p > L:
            break
        for j in range(i + 1, len(small_primes_one_mod_four)):
            q = small_primes_one_mod_four[j]
            fixed_pq = fixed_p * q ** e_q
            if fixed_pq > L:
                continue
            start_index = bisect.bisect_right(p1, q)
            K = L // fixed_pq
            if e_r == 1:
                contrib = compute_sum_over_primes_times_prefix(K, start_index, max_B, sum_prefix, p1, prefix_p1)
            else:
                contrib = 0
                max_r_power = int(K ** (1 / e_r)) if e_r > 0 else 0
                for k in range(start_index, len(p1)):
                    r = p1[k]
                    if r > max_r_power:
                        break
                    r_power = r ** e_r
                    m1 = fixed_pq * r_power
                    b_value = L // m1
                    su_value = sum_prefix[min(b_value, max_B)]
                    contrib += su_value * r_power
            total_sum_of_n += contrib * fixed_pq

print(total_sum_of_n)