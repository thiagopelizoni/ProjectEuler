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