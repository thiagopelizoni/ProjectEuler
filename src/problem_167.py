# Problem: https://projecteuler.net/problem=167
import collections

def z_array(d):
    n = len(d)
    z = [0] * n
    left = 0
    right = 0
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < n and d[z[i]] == d[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left = i
            right = i + z[i]
    return z

def get_min_period(d):
    n = len(d)
    z = z_array(d)
    for p in range(1, n):
        if z[p] == n - p:
            return p
    return n

def compute_ulam_term(b, target_k):
    sequence = [2, b]
    terms_set = set(sequence)
    current_last = b
    even_count = 1

    while even_count < 2:
        sums_count = collections.defaultdict(int)
        for i in range(len(sequence)):
            for j in range(i + 1, len(sequence)):
                current_sum = sequence[i] + sequence[j]
                if current_sum > current_last:
                    sums_count[current_sum] += 1
        candidate = current_last + 1
        while True:
            if sums_count[candidate] == 1:
                sequence.append(candidate)
                terms_set.add(candidate)
                current_last = candidate
                if candidate % 2 == 0:
                    even_count += 1
                break
            candidate += 1

    second_even = sequence[-1] if sequence[-1] % 2 == 0 else sequence[-2]

    max_num_terms = 10000000
    while len(sequence) < max_num_terms:
        candidate = current_last + 1
        while True:
            if candidate % 2 == 0:
                candidate += 1
                continue
            ways_count = 0
            if candidate - 2 in terms_set:
                ways_count += 1
            if candidate - second_even in terms_set:
                ways_count += 1
            if ways_count == 1:
                sequence.append(candidate)
                terms_set.add(candidate)
                current_last = candidate
                break
            candidate += 1

    start_periodic = sequence.index(second_even) + 1
    differences = [sequence[i + 1] - sequence[i] for i in range(start_periodic - 1, len(sequence) - 1)]

    max_preperiodic = 200
    preperiodic_length = -1
    period = -1
    for possible_pre in range(max_preperiodic):
        suffix_diffs = differences[possible_pre:]
        suffix_length = len(suffix_diffs)
        current_period = get_min_period(suffix_diffs)
        if current_period < suffix_length // 2 and suffix_length >= 3 * current_period:
            preperiodic_length = possible_pre
            period = current_period
            break

    if preperiodic_length == -1:
        raise ValueError("Period not found")

    initial_length = start_periodic + preperiodic_length
    if target_k <= initial_length:
        return sequence[target_k - 1]

    shift = target_k - initial_length
    cycle = differences[preperiodic_length:preperiodic_length + period]
    sum_cycle = sum(cycle)
    full_cycles = shift // period
    remainder = shift % period
    sum_prefix = sum(cycle[0:remainder])
    term = sequence[initial_length - 1] + full_cycles * sum_cycle + sum_prefix
    return term

sum_terms = 0
k = 10**11
for n in range(2, 11):
    b = 2 * n + 1
    term = compute_ulam_term(b, k)
    sum_terms += term

print(sum_terms)