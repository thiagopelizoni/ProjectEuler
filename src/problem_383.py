# Problem: https://projecteuler.net/problem=383
from functools import lru_cache

def get_base5_digits_lsd(n, base, length):
    digits = []
    tmp = n
    for _ in range(length):
        digits.append(tmp % base)
        tmp //= base
    return digits

def main():
    """
    Purpose

    Solves Project Euler problem 383, computing T_5(10^18), the number of integers i from 1 to
    10^18 satisfying f_5((2*i - 1)!) < 2 * f_5(i!), where f_5(k) is the highest power of 5
    dividing k.

    Parameters: None

    Returns: None, prints the result.

    Method / Math Rationale

    Equivalent to counting i <= 10^18 with s_5(2i - 1) >= 2 * s_5(i), where s_5 is the base-5
    digit sum. Use digit DP from LSD to MSD in base 5 with 27 digits (padded). State tracks
    position, comparison borrow (0/1) for i <= n via simulating n - i subtraction, whether
    still zero, running sums s_i and s_m, carry_in for doubling, borrow_in for subtraction.
    At each step, choose digit d (0-4), compute doubled digit with carry_in, get carry_out;
    subtract borrow_in to get m digit, get borrow_out. For comparison, compute effective
    n digit minus borrow_comp, subtract d, adjust if negative to get borrow_next. At end,
    handle possible extra digit for m, check no comparison borrow, and condition.

    Complexity

    O(l * 2 * 2 * s^2 * 2 * 2) states/transitions, with l=27, s~108, ~10^7 operations.

    References

    https://projecteuler.net/problem=383
    """

    n = 10**18
    base = 5
    l = 27
    digits = get_base5_digits_lsd(n, base, l)

    @lru_cache(maxsize=None)
    def dp(pos: int, borrow_comp: int, is_zero: bool, s_i: int, s_m: int, carry_in: int, borrow_in: int) -> int:
        if pos == l:
            if is_zero or borrow_comp != 0:
                return 0
            digit2i = carry_in
            digit_m = digit2i - borrow_in
            if digit_m < 0:
                if digit2i < borrow_in:
                    return 0
                digit_m += base
            new_s_m = s_m + digit_m
            if new_s_m >= 2 * s_i:
                return 1
            return 0

        ans = 0
        for d in range(base):
            new_is_zero = is_zero and (d == 0)
            new_s_i = s_i + (d if not new_is_zero else 0)
            temp = 2 * d + carry_in
            digit2i = temp % base
            carry_out = temp // base
            digit_m = digit2i - borrow_in
            borrow_out = 0
            if digit_m < 0:
                digit_m += base
                borrow_out = 1
            new_s_m = s_m + digit_m
            effective_n_d = digits[pos] - borrow_comp
            temp_comp = effective_n_d - d
            borrow_next = 0
            if temp_comp < 0:
                temp_comp += base
                borrow_next = 1
            ans += dp(pos + 1, borrow_next, new_is_zero, new_s_i, new_s_m, carry_out, borrow_out)
        return ans

    print(dp(0, 0, True, 0, 0, 0, 1))

if __name__ == "__main__":
    main()