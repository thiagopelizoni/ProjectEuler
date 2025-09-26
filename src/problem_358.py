# Problem: https://projecteuler.net/problem=358
import math
from sympy import isprime, factorint
from tqdm import tqdm

def get_first_digits(p, num_digits=11):
    digits = []
    rem = 1
    for _ in range(num_digits):
        rem *= 10
        digit = rem // p
        digits.append(str(digit))
        rem %= p
    return ''.join(digits)

def is_primitive_root(g, p):
    phi = p - 1
    factors = factorint(phi).keys()
    for q in factors:
        if pow(g, phi // q, p) == 1:
            return False
    return True

def main():
    """
    Purpose
    -------
    Computes the sum of all digits of the cyclic number that starts with 00000000137 and ends with 56789.

    Method / Math Rationale
    ------------------------
    The cyclic number is the repetend of 1/p for a prime p with full decimal period p-1 (10 is primitive root mod p).
    p satisfies p % 100000 = 9891 (from solving 56789 * p ≡ 99999 mod 100000 for the ending digits) and
    approximately 724637682 <= p <= 729927007 (from 1/p ≈ 1.37 * 10^{-9} for the starting digits).
    Confirm exact starting digits via long division. The digit sum is 9 * (p - 1) // 2 for such numbers.

    Complexity
    ----------
    Time: O(((p_max - p_min) / modulus) * log(p)^c) for primality and factoring, with small constants (53 iterations).
    Space: O(1)

    References
    ----------
    https://projecteuler.net/problem=358
    """
    min_frac = 1.37e-9
    max_frac = 1.38e-9
    p_min = math.ceil(1 / max_frac)
    p_max = math.floor(1 / min_frac)
    modulus = 100000
    inv = pow(56789, -1, modulus)
    target = (99999 * inv) % modulus
    remainder = p_min % modulus
    diff = (target - remainder) % modulus
    start = p_min + diff
    for p in tqdm(range(start, p_max + 1, modulus)):
        if isprime(p):
            if get_first_digits(p) == '00000000137':
                if is_primitive_root(10, p):
                    digit_sum = 9 * (p - 1) // 2
                    print(digit_sum)
                    break

if __name__ == "__main__":
    main()