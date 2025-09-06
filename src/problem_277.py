# Problem: https://projecteuler.net/problem=277
from fractions import Fraction
from math import gcd
from typing import Optional, Tuple

def mod_inverse(a: int, m: int) -> int:
    return pow(a, -1, m)

def solve_linear_congruence(a: int, b: int, m: int) -> Optional[Tuple[int, int]]:
    g: int = gcd(a, m)
    if b % g != 0:
        return None
    a_g: int = a // g
    b_g: int = b // g
    m_g: int = m // g
    inv: int = mod_inverse(a_g, m_g)
    x0: int = (inv * b_g) % m_g
    return x0, m_g

def main() -> None:
    """Purpose:
    Solves Project Euler problem 277: finds the smallest integer a1 > 10^15 whose
    modified Collatz sequence begins with the specified step sequence.

    Method / Math Rationale:
    Composes backward affine transformations using fractions for the inverse steps.
    Derives a1 = coeff * k + const. Solves the linear congruence to find k values
    yielding integer a1. Computes the smallest such a1 exceeding 10^15 by advancing
    in the arithmetic progression.

    Complexity:
    Time: O(1), Space: O(1)

    References:
    https://projecteuler.net/problem=277
    """
    s: str = "UDDDUdddDDUDDddDdDddDDUDDdUUDd"
    target: int = 10**15
    steps_reversed: list[str] = list(s[::-1])
    coeff: Fraction = Fraction(1)
    const: Fraction = Fraction(0)
    for step in steps_reversed:
        if step == 'D':
            div: int = 1
            add: int = 0
        elif step == 'U':
            div = 4
            add = -2
        elif step == 'd':
            div = 2
            add = 1
        coeff = coeff * Fraction(3, div)
        const = const * Fraction(3, div) + Fraction(add, div)
    c_den: int = coeff.denominator
    b_den: int = const.denominator
    lcm_den: int = c_den * b_den // gcd(c_den, b_den)
    multiplier_k: int = coeff.numerator * (lcm_den // c_den)
    constant_term: int = const.numerator * (lcm_den // b_den)
    mod: int = lcm_den
    a: int = multiplier_k % mod
    bb: int = (-constant_term) % mod
    result = solve_linear_congruence(a, bb, mod)
    if result is None:
        raise ValueError("No solution")
    k0, step = result
    k: int = k0 if k0 != 0 else step
    a1: int = (multiplier_k * k + constant_term) // lcm_den
    if a1 > target:
        print(a1)
        return
    increment: int = (multiplier_k * step) // lcm_den
    to_add: int = target + 1 - a1
    t: int = (to_add + increment - 1) // increment
    k = k + step * t
    a1 = (multiplier_k * k + constant_term) // lcm_den
    print(a1)

if __name__ == "__main__":
    main()