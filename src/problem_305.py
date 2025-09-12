# Problem: https://projecteuler.net/problem=305
import math
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


def get_failure(s):
    l = len(s)
    failure = [0] * l
    j = 0
    for i in range(1, l):
        while j > 0 and s[i] != s[j]:
            j = failure[j - 1]
        if s[i] == s[j]:
            j += 1
        failure[i] = j
    return failure


def transition(state, char, s, failure):
    j = state
    while j > 0 and char != s[j]:
        j = failure[j - 1]
    if char == s[j]:
        j += 1
    return j


def count_within(kk, s):
    if kk <= 0:
        return 0
    ds = str(kk)
    length = len(ds)
    digits = [int(c) for c in ds]
    memo = {}
    ways_memo = {}
    failure = get_failure(s)
    l = len(s)

    def ways(pos, tight, started):
        if pos == length:
            return 1 if started else 0
        key = (pos, tight, started)
        if key in ways_memo:
            return ways_memo[key]
        ans = 0
        up = digits[pos] if tight else 9
        for dd in range(up + 1):
            new_tight = 1 if tight and dd == digits[pos] else 0
            new_started = started or dd > 0
            ans += ways(pos + 1, new_tight, new_started)
        ways_memo[key] = ans
        return ans

    def dfs(pos, match, tight, started):
        if pos == length:
            return 0
        key = (pos, match, tight, started)
        if key in memo:
            return memo[key]
        ans = 0
        up = digits[pos] if tight else 9
        for dd in range(up + 1):
            new_tight = 1 if tight and dd == digits[pos] else 0
            new_started = started or dd > 0
            if not new_started:
                new_match = 0
                add = 0
            else:
                char = str(dd)
                new_match = transition(match, char, s, failure)
                add = ways(pos + 1, new_tight, new_started) if new_match == l else 0
                if new_match == l:
                    new_match = failure[l - 1]
            ans += add + dfs(pos + 1, new_match, new_tight, new_started)
        memo[key] = ans
        return ans

    return dfs(0, 0, 1, 0)


def count_spanning(mm, s, small_count, small_max, num_valid_j):
    if mm < 1:
        return 0
    l = len(s)
    if mm < small_max:
        count = 0
        for i in range(1, mm + 1):
            i_str = str(i)
            ip1_str = str(i + 1)
            for j in range(1, l):
                if j <= len(i_str) and (l - j) <= len(ip1_str):
                    if i_str[-j:] == s[:j] and ip1_str[:(l - j)] == s[j:]:
                        count += 1
        return count
    count = small_count
    d = len(str(mm))
    for D in range(l + 1, d):
        count += 10 ** (D - l) * num_valid_j
    for power in range(l, d):
        i_str = "9" * power
        ip1_str = "1" + "0" * power
        for j in range(1, l):
            if j <= power and (l - j) <= (power + 1):
                if i_str[-j:] == s[:j] and ip1_str[:(l - j)] == s[j:]:
                    count += 1
    start_current = 10 ** (d - 1)
    for j in range(1, l):
        if s[j] == "0":
            continue
        lj = l - j
        prefix_str = s[j:]
        suffix_str = s[:j]
        prefix = int(prefix_str)
        suffix = int(suffix_str)
        mid_len = d - l
        step = 10 ** j
        base = prefix * (10 ** (d - lj)) + suffix
        if mid_len < 0:
            continue
        if mid_len == 0:
            i = base
            if start_current <= i <= mm:
                count += 1
            continue
        min_middle = 0
        if base < start_current:
            diff = start_current - base
            min_middle = math.ceil(diff / step)
        max_middle = (mm - base) // step
        max_middle = min(max_middle, 10 ** mid_len - 1)
        if max_middle >= min_middle and min_middle >= 0:
            count += max_middle - min_middle + 1
    return count


def cum_digits_up_to(kk):
    if kk <= 0:
        return 0
    ds = str(kk)
    d = len(ds)
    total = 0
    power = 1
    for dd in range(1, d):
        num_nums = 9 * power
        total += num_nums * dd
        power *= 10
    start_current = power
    num_current = kk - start_current + 1
    total += num_current * d
    return total


def compute_f(m):
    s = str(m)
    l = len(s)
    small_max = 10 ** l - 1
    small_count = 0
    for i in tqdm(range(1, small_max)):
        i_str = str(i)
        ip1_str = str(i + 1)
        for j in range(1, l):
            if j <= len(i_str) and (l - j) <= len(ip1_str):
                if i_str[-j:] == s[:j] and ip1_str[:(l - j)] == s[j:]:
                    small_count += 1
    num_valid_j = sum(1 for j in range(1, l) if s[j] != "0")
    low = 1
    high = 10 ** 15
    while low < high:
        mid = (low + high) // 2
        if count_within(mid, s) + count_spanning(mid - 1, s, small_count, small_max, num_valid_j) >= m:
            high = mid
        else:
            low = mid + 1
    k = low
    total_prev = count_within(k - 1, s) + count_spanning(k - 2, s, small_count, small_max, num_valid_j) if k > 1 else 0
    remaining = m - total_prev
    spanning_starts = []
    if k > 1:
        i_str = str(k - 1)
        ip1_str = str(k)
        D = len(i_str)
        for j in range(1, l):
            if j <= D and (l - j) <= len(ip1_str):
                if i_str[-j:] == s[:j] and ip1_str[:(l - j)] == s[j:]:
                    rel_start = D - j + 1
                    spanning_starts.append(rel_start)
    spanning_starts.sort()
    num_span = len(spanning_starts)
    if remaining <= num_span:
        rel = spanning_starts[remaining - 1]
        cum_to_k2 = cum_digits_up_to(k - 2) if k > 1 else 0
        pos = cum_to_k2 + rel
        return pos
    remaining -= num_span
    k_str = str(k)
    Dk = len(k_str)
    within_starts = []
    curr_match = 0
    failure = get_failure(s)
    for ii in range(Dk):
        char = k_str[ii]
        curr_match = transition(curr_match, char, s, failure)
        if curr_match == l:
            rel_start = ii - l + 2
            within_starts.append(rel_start)
            curr_match = failure[l - 1]
    rel = within_starts[remaining - 1]
    cum_to_k1 = cum_digits_up_to(k - 1)
    pos = cum_to_k1 + rel
    return pos


def main():
    """
    Purpose:
    Solves Project Euler problem 305 by computing the sum of f(3^k) for k from 1 to 13, where f(n) is the starting position
    of the nth occurrence of the string representation of n in the concatenated positive integers.

    Method / Math Rationale:
    For each power m = 3^k, uses binary search to find the minimal integer k such that the total occurrences of str(m)
    in the concatenation of 1 to k is at least m. Occurrences include within-number matches counted via digit DP with
    a string matching automaton and spanning matches across consecutive numbers. Spanning matches are computed exactly
    for small digit lengths and using closed-form arithmetic progressions for larger lengths. The exact position is then
    located by identifying whether the target occurrence is a spanning or within match in the final number.

    Complexity:
    O(13 * log(10^15) * (digit DP states ~ 15*10*2*2 * 10) + small loop max 10^7 per power) operations, parallelized
    across the 13 computations.

    References:
    https://projecteuler.net/problem=305
    """
    powers = [3 ** i for i in range(1, 14)]
    with ProcessPoolExecutor() as executor:
        fs = list(tqdm(executor.map(compute_f, powers), total=13, desc="Computing f(3^k)"))
    sum_b = sum(fs)
    print(sum_b)


if __name__ == "__main__":
    main()