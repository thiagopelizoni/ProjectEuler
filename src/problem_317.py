# Problem: https://projecteuler.net/problem=317
from decimal import Decimal, getcontext


def main():
    """
    Purpose
    -------
    Compute the volume (m³) occupied by all fragments of a firecracker that
    explodes 100 m above the ground, with fragment speeds up to 20 m/s, as posed
    in Project Euler problem 317.

    Method / Math Rationale
    -----------------------
    For an initial speed `V` and launch angle θ, the fragment’s trajectory is
        x(t) = V cos θ t,
        y(t) = H + V sin θ t − ½ g t².
    Eliminating *t* and maximising *y* for fixed horizontal distance *x* (with
    `v = V`) gives the envelope
        y_max(x) = H + V²/(2g) − g x²/(2V²).
    The farthest horizontal reach is
        r_max² = (2 V² H)/g + V⁴/g².
    Revolving the 2-D envelope around the vertical axis, the volume is
        Vol = 2 π ∫₀^{r_max} y_max(r) r dr
            = π V²/g · [ H² + (V²/g) H + (V²/g)²/4 ].

    Complexity
    ----------
    O(1) time, O(1) space.

    References
    ----------
    https://projecteuler.net/problem=317
    """
    getcontext().prec = 50

    # Constants
    H = Decimal("100")      # height in metres
    V = Decimal("20")       # maximum fragment speed (m/s)
    g = Decimal("9.81")     # gravitational acceleration (m/s²)
    pi = Decimal("3.14159265358979323846264338327950288419716939937510")

    a = V ** 2 / g  # V² / g
    bracket = H ** 2 + a * H + a ** 2 / Decimal(4)
    volume = pi * a * bracket

    print(f"{volume:.4f}")


if __name__ == "__main__":
    main()