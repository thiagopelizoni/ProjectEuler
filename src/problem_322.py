# Problem: https://projecteuler.net/problem=322
import bisect
import sys
from functools import lru_cache
import numpy as np
from numba import njit
from tqdm import tqdm

def get_digits(x, base):
    if x == 0:
        return [0]
    digits = []
    while x > 0:
        digits.append(x % base)
        x //= base
    digits.reverse()
    return digits

def generate_residues(pos, current, p, pow_p, upper_d, residues):
    if pos == len(upper_d):
        residues.append(current)
        return
    max_d = upper_d[pos]
    cur_pow = pow_p[pos]
    for d in range(max_d + 1):
        generate_residues(pos + 1, current + d * cur_pow, p, pow_p, upper_d, residues)

@lru_cache(None)
def count_below_dp(pos, tight, L, digs_rem, constrained):
    if pos == L:
        return 1
    ans = 0
    up = digs_rem[pos] if tight else 1
    for d in range(up + 1):
        bit_idx = L - 1 - pos
        if constrained[bit_idx] and d == 1:
            continue
        new_tight = tight and (d == up)
        ans += count_below_dp(pos + 1, new_tight, L, digs_rem, constrained)
    return ans

def main():
    """
    Purpose
    Solves Project Euler Problem 322: Find T(10^18, 10^12-10), where T(m, n) is the number of binomial coefficients
    C(i, n) divisible by 10 for n ≤ i < m.

    Method / Math Rationale
    T(m, n) = (m - n) - number of C(i, n) not div by 10 for i in [n, m).
    Number not div by 10 = num(not div 2) + num(not div 5) - num(not div 2 and not div 5)
    By Kummer's theorem, v_p(C(i, n)) = number of carries when adding n + (i - n) in base p.
    num(not div p) = count of k = i - n in [0, m - n) where no carries, i.e. digits(k) <= p-1 - digits(n) componentwise in base p.
    Computed using periodicity: period = p^{len(digits_n(p))}, valid residues mod period generated recursively,
    then count = full periods * valid count + count in remainder using bisect.
    For both: loop over full periods and valid residues, check if (period * i + a) & n == 0 using mod 2^{bit_length(n)}.

    Complexity
    O(L log_p(m)) for residue generation (small); O(full periods * valid residues) ~ 1.26e9 for both, optimized with njit;
    O(L) for digit DP in base 2 remainder.

    References
    https://projecteuler.net/problem=322
    """
    n = 10**12 - 10
    m = 10**18
    S = m - n
    L2 = n.bit_length()
    period2 = 1 << L2
    popcount = bin(n).count('1')
    num_per2 = 1 << (L2 - popcount)
    rem2 = S % period2
    digs_rem2 = get_digits(rem2, 2)
    L_rem2 = len(digs_rem2)
    digs_rem2 = [0] * (L2 - L_rem2) + digs_rem2
    constrained = [(n & (1 << j)) != 0 for j in range(L2)]
    count_extra2 = count_below_dp(0, True, L2, tuple(digs_rem2), tuple(constrained))
    num_not2 = (S // period2) * num_per2 + count_extra2
    p = 5
    digs_n5 = get_digits(n, p)
    L5 = len(digs_n5)
    period5 = pow(p, L5)
    upper_d = [p - 1 - d for d in digs_n5[::-1]]
    pow_p = [pow(p, i) for i in range(L5)]
    residues = []
    generate_residues(0, 0, p, pow_p, upper_d, residues)
    vec5 = sorted(residues)
    rem5 = S % period5
    count_extra5 = bisect.bisect_left(vec5, rem5)
    num_not5 = (S // period5) * len(vec5) + count_extra5
    two40 = 1 << 40
    period5_mod_two40 = period5 % two40
    vec5_arr = np.array(vec5, dtype=np.int64)

    @njit
    def count_both_full(num_full, period5_mod_two40, two40, n, vec5_arr):
        cnt = 0
        for i in range(num_full):
            base = i * period5_mod_two40 % two40
            for idx in range(vec5_arr.size):
                a = vec5_arr[idx]
                mod2 = (base + (a % two40)) % two40
                if (mod2 & n) == 0:
                    cnt += 1
        return cnt

    num_full = int(S // period5)
    num_both = count_both_full(num_full, period5_mod_two40, two40, n, vec5_arr)

    base_rem = num_full * period5_mod_two40 % two40
    for a in vec5:
        if a >= rem5:
            continue
        mod2 = (base_rem + (a % two40)) % two40
        if (mod2 & n) == 0:
            num_both += 1
    not10 = num_not2 + num_not5 - num_both
    T = S - not10
    print(T)

if __name__ == "__main__":
    main()