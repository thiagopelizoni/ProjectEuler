# Problem: https://projecteuler.net/problem=548
import sys
import numpy as np
from numba import njit
from functools import lru_cache
import itertools

@njit(fastmath=True, cache=True)
def get_prime_signature_fast(n):
    if n == 1:
        return np.array([0], dtype=np.int64)[:0]
    exponents = np.zeros(60, dtype=np.int64)
    count_idx = 0
    temp = n
    if temp % 2 == 0:
        cnt = 0
        while temp % 2 == 0:
            cnt += 1
            temp //= 2
        exponents[count_idx] = cnt
        count_idx += 1
    if temp % 3 == 0:
        cnt = 0
        while temp % 3 == 0:
            cnt += 1
            temp //= 3
        exponents[count_idx] = cnt
        count_idx += 1
    d = 5
    limit = int(temp**0.5)
    while d <= limit:
        if temp % d == 0:
            cnt = 0
            while temp % d == 0:
                cnt += 1
                temp //= d
            exponents[count_idx] = cnt
            count_idx += 1
            limit = int(temp**0.5)
        d += 2
        if temp % d == 0:
            cnt = 0
            while temp % d == 0:
                cnt += 1
                temp //= d
            exponents[count_idx] = cnt
            count_idx += 1
            limit = int(temp**0.5)
        d += 4
    if temp > 1:
        exponents[count_idx] = 1
        count_idx += 1
    valid_exps = exponents[:count_idx]
    for i in range(count_idx):
        for j in range(i + 1, count_idx):
            if valid_exps[j] > valid_exps[i]:
                valid_exps[i], valid_exps[j] = valid_exps[j], valid_exps[i]
    return valid_exps

@njit(cache=True)
def check_signature_match(sig_target, sig_candidate):
    if len(sig_target) != len(sig_candidate):
        return False
    for i in range(len(sig_target)):
        if sig_target[i] != sig_candidate[i]:
            return False
    return True

@lru_cache(maxsize=None)
def calc_g_signature(sig):
    if not sig:
        return 1
    ranges = [range(x + 1) for x in sig]
    total = 0
    for p in itertools.product(*ranges):
        if p == sig:
            continue
        sub_sig = tuple(sorted((x for x in p if x > 0), reverse=True))
        total += calc_g_signature(sub_sig)
    return total

def main():
    total_sum = 0
    MAX_EXPONENT_SUM = 60 
    LIMIT_VAL = 2 * 10**16
    stack = [(1,)]
    total_sum += 1
    visited = set()
    visited.add((1,))
    while stack:
        curr_sig = stack.pop()
        g_val = calc_g_signature(curr_sig)
        if g_val > LIMIT_VAL:
            continue
        actual_sig_arr = get_prime_signature_fast(g_val)
        if check_signature_match(curr_sig, actual_sig_arr):
            total_sum += g_val
        if sum(curr_sig) >= MAX_EXPONENT_SUM:
            continue
        can_increment = False
        if len(curr_sig) == 1:
            can_increment = True
        elif curr_sig[-2] > curr_sig[-1]:
            can_increment = True
        if can_increment:
            new_sig_list = list(curr_sig)
            new_sig_list[-1] += 1
            new_sig = tuple(new_sig_list)
            if new_sig not in visited:
                visited.add(new_sig)
                stack.append(new_sig)
        new_sig_append = curr_sig + (1,)
        if new_sig_append not in visited:
            visited.add(new_sig_append)
            stack.append(new_sig_append)
    print(total_sum)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()