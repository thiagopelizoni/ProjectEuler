# Problem: https://projecteuler.net/problem=449
import math

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 449 by calculating the volume of a 1 mm thick chocolate
    coating around an ellipsoidal candy center with a=3 mm, b=1 mm.

    Method / Math Rationale
    ------------------------
    The candy center is an oblate spheroid with semi-axes 3, 3, 1 mm. The chocolate
    volume is the volume of the parallel body at distance 1 mm minus the inner volume,
    given by Steiner formula:  S * r + pi * V_1 * r^2 + (4/3) pi * r^3, where S is the
    surface area, and V_1 is the intrinsic volume related to the integral of the
    support function over the unit sphere, computed using the formula for mean width
    or direct calculation.

    Complexity
    ----------
    O(1), constant time computations.

    References
    ----------
    https://projecteuler.net/problem=449
    """
    a = 3
    b = 1
    r = 1
    e = math.sqrt(1 - (b / a)**2)
    S = 2 * math.pi * a**2 + math.pi * (b**2 / e) * math.log((1 + e) / (1 - e))
    V_2 = S / 2
    int_val = a * (1 / (2 * e)) * (math.asin(e) + e * math.sqrt(1 - e**2))
    V_1 = 4 * int_val
    vol_choc = 2 * V_2 * r + math.pi * V_1 * r**2 + (4 / 3) * math.pi * r**3
    print(f"{vol_choc:.8f}")

if __name__ == "__main__":
    main()