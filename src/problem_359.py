# Problem: https://projecteuler.net/problem=359
from math import pow

def P(floor, room):
    result = (floor + 1) // 2 * floor
    if floor % 2 == 1 and floor > 1:
        result -= (floor + 1) // 2
    increment_even = 1
    if floor % 2 == 0:
        increment_even = 2 * floor + 1
    increment_odd = 2
    if floor % 2 == 1:
        increment_odd = 2 * floor
    if floor == 1:
        increment_odd = 3
        increment_even = 2
    num_even = room // 2
    triangle_even = num_even * (num_even + 1)
    num_odd = (room - 1) // 2
    triangle_odd = num_odd * (num_odd + 1)
    result += num_even * (increment_even - 2) + triangle_even
    result += num_odd * (increment_odd - 2) + triangle_odd
    return result

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 359 by computing the sum of P(f, r) for all
    positive integers f and r such that f * r = 71328803586048, and prints the
    last 8 digits of this sum.
    Parameters: None
    Returns: None (prints the result)

    Method / Math Rationale
    ------------------------
    Uses a closed-form formula for P(f, r), the person number occupying room r
    in floor f, derived from patterns in room assignments. The first person in
    each floor is calculated based on floor parity. Subsequent persons are added
    using arithmetic progressions for odd and even room positions, with
    increments depending on floor parity. The sum is computed over all divisor
    pairs (f, r) of the given number.

    Complexity
    ----------
    O(1) per P computation, with a constant number of divisor pairs (364),
    resulting in overall constant time complexity O(1).

    References
    ----------
    https://projecteuler.net/problem=359
    """
    N = 71328803586048
    mod = 100000000
    exp_two = 27
    exp_three = 12
    total_sum = 0
    for a in range(exp_two + 1):
        pow_two = 1 << a
        for b in range(exp_three + 1):
            pow_three = int(pow(3, b))
            f = pow_two * pow_three
            r = N // f
            total_sum += P(f, r)
    print(total_sum % mod)

if __name__ == "__main__":
    main()