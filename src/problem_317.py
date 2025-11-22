# Problem: https://projecteuler.net/problem=317
from decimal import Decimal, getcontext


def main():
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