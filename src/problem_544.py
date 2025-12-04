import numpy as np
from numba import njit, prange, int64
from numba.typed import Dict

MOD = 1_000_000_007
ROWS = 9
COLS = 10
TARGET_N = 1112131415
DEGREE = ROWS * COLS
POINTS_NEEDED = DEGREE + 2

@njit(fastmath=True, cache=True)
def pack_state(state_arr):
    res = 0
    for i in range(9):
        res |= (int64(state_arr[i]) << (4 * i))
    return res

@njit(fastmath=True, cache=True)
def unpack_state(packed, out_arr):
    for i in range(9):
        out_arr[i] = (packed >> (4 * i)) & 0xF

@njit(fastmath=True, cache=True)
def canonicalize(arr):
    mapping = -np.ones(16, dtype=np.int8)
    next_id = 0
    res = 0
    for i in range(9):
        val = arr[i]
        c = mapping[val]
        if c == -1:
            c = next_id
            mapping[val] = c
            next_id += 1
        res |= (int64(c) << (4 * i))
    return res, next_id

@njit(fastmath=True, cache=True)
def mod_mul(a, b):
    return (a * b) % MOD

@njit(fastmath=True, cache=True)
def mod_add(a, b):
    return (a + b) % MOD

@njit(parallel=True, fastmath=True, cache=True)
def compute_points(num_points):
    results = np.zeros(num_points, dtype=np.int64)
    for x in prange(num_points):
        curr_dp = Dict.empty(key_type=int64, value_type=int64)
        initial_packed = 0
        curr_dp[initial_packed] = 1
        temp_state = np.zeros(9, dtype=np.int8)
        temp_next = np.zeros(9, dtype=np.int8)
        for c in range(COLS):
            for r in range(ROWS):
                next_dp = Dict.empty(key_type=int64, value_type=int64)
                for packed_s, count in curr_dp.items():
                    if count == 0: continue
                    unpack_state(packed_s, temp_state)
                    val_left = temp_state[r]
                    val_up = temp_state[r-1] if r > 0 else -1
                    used_mask = 0
                    max_id = -1
                    for k in range(9):
                        val = temp_state[k]
                        used_mask |= (1 << val)
                        if val > max_id: max_id = val
                    distinct_count = 0
                    for k in range(10):
                        if (used_mask >> k) & 1:
                            distinct_count += 1
                    for k in range(max_id + 1):
                        if (used_mask >> k) & 1:
                            if c > 0 and k == val_left:
                                continue
                            if r > 0 and k == val_up:
                                continue
                            for i in range(9): temp_next[i] = temp_state[i]
                            temp_next[r] = k
                            can_packed, _ = canonicalize(temp_next)
                            if can_packed in next_dp:
                                next_dp[can_packed] = mod_add(next_dp[can_packed], count)
                            else:
                                next_dp[can_packed] = count
                    weight = x - distinct_count
                    if weight > 0:
                        for i in range(9): temp_next[i] = temp_state[i]
                        temp_next[r] = max_id + 1
                        can_packed, _ = canonicalize(temp_next)
                        term = mod_mul(count, weight % MOD)
                        if can_packed in next_dp:
                            next_dp[can_packed] = mod_add(next_dp[can_packed], term)
                        else:
                            next_dp[can_packed] = term
                curr_dp = next_dp
        total = 0
        for v in curr_dp.values():
            total = mod_add(total, v)
        results[x] = total
    return results

@njit(fastmath=True)
def mod_pow(base, exp):
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

@njit(fastmath=True)
def mod_inverse(n):
    return mod_pow(n, MOD - 2)

@njit(fastmath=True, cache=True)
def lagrange_interpolate_sum(y_values, target_n):
    k = len(y_values) - 1
    if target_n <= k:
        return y_values[target_n]
    fact = np.ones(k + 1, dtype=np.int64)
    inv_fact = np.ones(k + 1, dtype=np.int64)
    for i in range(1, k + 1):
        fact[i] = (fact[i-1] * i) % MOD
    inv_fact[k] = mod_inverse(fact[k])
    for i in range(k - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
    prefix = np.ones(k + 1, dtype=np.int64)
    suffix = np.ones(k + 1, dtype=np.int64)
    for i in range(k):
        prefix[i+1] = (prefix[i] * ((target_n - i) % MOD)) % MOD
    for i in range(k, 0, -1):
        suffix[i-1] = (suffix[i] * ((target_n - i) % MOD)) % MOD
    ans = 0
    for i in range(k + 1):
        numerator = (prefix[i] * suffix[i]) % MOD
        denominator = (inv_fact[i] * inv_fact[k-i]) % MOD
        sign = 1 if (k - i) % 2 == 0 else -1
        term = (y_values[i] * numerator) % MOD
        term = (term * denominator) % MOD
        if sign == -1:
            ans = (ans - term + MOD) % MOD
        else:
            ans = (ans + term) % MOD
    return ans

def main():
    p_values = compute_points(POINTS_NEEDED)
    s_values = np.zeros(POINTS_NEEDED, dtype=np.int64)
    current_sum = 0
    for x in range(POINTS_NEEDED):
        if x == 0:
            s_values[x] = 0
        else:
            current_sum = (current_sum + p_values[x]) % MOD
            s_values[x] = current_sum
    result = lagrange_interpolate_sum(s_values, TARGET_N)
    print(result)

if __name__ == "__main__":
    main()