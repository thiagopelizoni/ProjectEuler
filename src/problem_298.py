# Problem: https://projecteuler.net/problem=298
from fractions import Fraction
from collections import deque

def update_for_outside(l_size, r_size, pairs):
    new_pairs = set(pairs)
    delta = 0
    # Larry miss
    evict_l = (l_size == 5)
    new_l_size = min(5, l_size + 1)
    if evict_l:
        # evict 4
        to_remove = None
        for r in range(r_size):
            if (4, r) in new_pairs:
                to_remove = (4, r)
                break
        if to_remove:
            new_pairs.remove(to_remove)
    # shift l_pos up
    shifted_pairs = set()
    for l, r in new_pairs:
        if not evict_l or l < 4:
            shifted_pairs.add((l + 1, r))
    new_pairs = shifted_pairs
    new_l_pos = 0
    # Robin miss
    evict_r = (r_size == 5)
    new_r_size = min(5, r_size + 1)
    new_r_pos = 4 if evict_r else r_size
    if evict_r:
        # evict 0
        to_remove = None
        for l in range(new_l_size):
            if (l, 0) in new_pairs:
                to_remove = (l, 0)
                break
        if to_remove:
            new_pairs.remove(to_remove)
        # shift r_pos down
        shifted_pairs = set()
        for l, r in new_pairs:
            shifted_pairs.add((l, r - 1))
        new_pairs = shifted_pairs
    # add new pair
    new_pairs.add((new_l_pos, new_r_pos))
    return new_l_size, new_r_size, new_pairs, delta

def update_for_shared(l_size, r_size, pairs, p):
    l, r = p
    new_pairs = set(pairs)
    delta = 0
    # Larry hit at l
    # move l to 0, shift 0 to l-1 to 1 to l
    shifted_pairs = set()
    for old_l, old_r in new_pairs:
        if old_l == l:
            shifted_pairs.add((0, old_r))
        elif old_l < l:
            shifted_pairs.add((old_l + 1, old_r))
        else:
            shifted_pairs.add((old_l, old_r))
    new_pairs = shifted_pairs
    # Robin hit, no change
    return l_size, r_size, new_pairs, delta

def update_for_only_l(l_size, r_size, pairs, l):
    new_pairs = set(pairs)
    delta = 1
    # Larry hit at l
    shifted_pairs = set()
    for old_l, old_r in new_pairs:
        if old_l == l:
            shifted_pairs.add((0, old_r))
        elif old_l < l:
            shifted_pairs.add((old_l + 1, old_r))
        else:
            shifted_pairs.add((old_l, old_r))
    new_pairs = shifted_pairs
    # Robin miss
    evict_r = (r_size == 5)
    new_r_size = min(5, r_size + 1)
    new_r_pos = 4 if evict_r else r_size
    if evict_r:
        to_remove = None
        for ll in range(l_size):
            if (ll, 0) in new_pairs:
                to_remove = (ll, 0)
                break
        if to_remove:
            new_pairs.remove(to_remove)
        shifted_pairs = set()
        for ll, rr in new_pairs:
            shifted_pairs.add((ll, rr - 1))
        new_pairs = shifted_pairs
    # add pair (0, new_r_pos) since the called is now at 0 in L
    new_pairs.add((0, new_r_pos))
    return l_size, new_r_size, new_pairs, delta

def update_for_only_r(l_size, r_size, pairs, r):
    new_pairs = set(pairs)
    delta = -1
    # Larry miss
    evict_l = (l_size == 5)
    new_l_size = min(5, l_size + 1)
    if evict_l:
        to_remove = None
        for rr in range(r_size):
            if (4, rr) in new_pairs:
                to_remove = (4, rr)
                break
        if to_remove:
            new_pairs.remove(to_remove)
    shifted_pairs = set()
    for ll, rr in new_pairs:
        if not evict_l or ll < 4:
            shifted_pairs.add((ll + 1, rr))
    new_pairs = shifted_pairs
    new_l_pos = 0
    # Robin hit, no change
    # add pair (new_l_pos, r)
    new_pairs.add((new_l_pos, r))
    return new_l_size, r_size, new_pairs, delta

def generate_states():
    initial = (0, 0, frozenset())
    seen = set([initial])
    queue = deque([initial])
    while queue:
        current = queue.popleft()
        l_size, r_size, pairs = current
        c = len(pairs)
        distinct_in_mem = l_size + r_size - c
        outside = 10 - distinct_in_mem
        if outside > 0:
            new_l, new_r, new_p, _ = update_for_outside(l_size, r_size, pairs)
            new_key = (new_l, new_r, frozenset(new_p))
            if new_key not in seen:
                seen.add(new_key)
                queue.append(new_key)
        for p in pairs:
            new_l, new_r, new_p, _ = update_for_shared(l_size, r_size, pairs, p)
            new_key = (new_l, new_r, frozenset(new_p))
            if new_key not in seen:
                seen.add(new_key)
                queue.append(new_key)
        only_l_pos = set(range(l_size)) - set(ll for ll, rr in pairs)
        for pos in only_l_pos:
            new_l, new_r, new_p, _ = update_for_only_l(l_size, r_size, pairs, pos)
            new_key = (new_l, new_r, frozenset(new_p))
            if new_key not in seen:
                seen.add(new_key)
                queue.append(new_key)
        only_r_pos = set(range(r_size)) - set(rr for ll, rr in pairs)
        for pos in only_r_pos:
            new_l, new_r, new_p, _ = update_for_only_r(l_size, r_size, pairs, pos)
            new_key = (new_l, new_r, frozenset(new_p))
            if new_key not in seen:
                seen.add(new_key)
                queue.append(new_key)
    return list(seen)

def main():
    """
    Purpose
    Solve Project Euler problem 298: compute the expected value of |L - R| after 50 turns in the memory game.

    Method / Math Rationale
    Uses dynamic programming over reachable states of the memories' configurations, tracking the probability distribution over the score difference for each state.
    The state is defined by the current sizes of the memories and the set of matched positions between them.
    Transitions are computed for each possible type of number called (shared, only in Larry, only in Robin, outside).
    The expected value is the weighted sum of |d| over all probabilities at the final turn.

    Complexity
    O(T * S * D * K) where T=50 turns, S≈439 states, D=101 differences, K≈10 transitions per state; highly efficient.

    References
    https://projecteuler.net/problem=298
    """
    states = generate_states()
    num_states = len(states)
    state_id = {states[i]: i for i in range(num_states)}
    MAX_D = 50
    OFFSET = MAX_D
    prob = [[Fraction(0) for _ in range(2 * MAX_D + 1)] for _ in range(num_states)]
    initial_id = state_id[(0, 0, frozenset())]
    prob[initial_id][OFFSET] = Fraction(1)
    for t in range(50):
        new_prob = [[Fraction(0) for _ in range(2 * MAX_D + 1)] for _ in range(num_states)]
        for s in range(num_states):
            for dd in range(-t, t + 1):
                p = prob[s][dd + OFFSET]
                if p == 0:
                    continue
                l_size, r_size, pairs = states[s]
                c = len(pairs)
                distinct_in_mem = l_size + r_size - c
                outside = 10 - distinct_in_mem

                if outside > 0:
                    new_l, new_r, new_p, delta = update_for_outside(l_size, r_size, pairs)
                    new_key = (new_l, new_r, frozenset(new_p))
                    new_s = state_id[new_key]
                    trans_p = Fraction(outside, 10)
                    new_dd = dd + delta
                    new_prob[new_s][new_dd + OFFSET] += p * trans_p

                for pp in pairs:
                    new_l, new_r, new_p, delta = update_for_shared(l_size, r_size, pairs, pp)
                    new_key = (new_l, new_r, frozenset(new_p))
                    new_s = state_id[new_key]
                    trans_p = Fraction(1, 10)
                    new_dd = dd + delta
                    new_prob[new_s][new_dd + OFFSET] += p * trans_p

                only_l_pos = set(range(l_size)) - {ll for ll, rr in pairs}
                for pos in only_l_pos:
                    new_l, new_r, new_p, delta = update_for_only_l(l_size, r_size, pairs, pos)
                    new_key = (new_l, new_r, frozenset(new_p))
                    new_s = state_id[new_key]
                    trans_p = Fraction(1, 10)
                    new_dd = dd + delta
                    new_prob[new_s][new_dd + OFFSET] += p * trans_p

                only_r_pos = set(range(r_size)) - {rr for ll, rr in pairs}
                for pos in only_r_pos:
                    new_l, new_r, new_p, delta = update_for_only_r(l_size, r_size, pairs, pos)
                    new_key = (new_l, new_r, frozenset(new_p))
                    new_s = state_id[new_key]
                    trans_p = Fraction(1, 10)
                    new_dd = dd + delta
                    new_prob[new_s][new_dd + OFFSET] += p * trans_p
        prob = new_prob

    expected = Fraction(0)
    for s in range(num_states):
        for dd in range(-50, 51):
            expected += prob[s][dd + OFFSET] * abs(dd)

    print("{:.8f}".format(float(expected)))

if __name__ == "__main__":
    main()