# Problem: https://projecteuler.net/problem=363
from mpmath import mp, quad, sqrt, pi

def dxdt(t, v):
    return (6 * v - 6) * t + (6 - 9 * v) * t**2

def dydt(t, v):
    return 3 * v + (6 - 12 * v) * t + (9 * v - 6) * t**2

def integrand(t, v):
    return sqrt(dxdt(t, v)**2 + dydt(t, v)**2)

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 363 by finding the value v for the Bézier curve such that the enclosed area is π/4,
    computes the arc length L of the curve, and calculates the percentage difference from the quarter circle arc
    length, printing the result rounded to 10 decimal places.

    Method / Math Rationale
    -----------------------
    Solves the quadratic equation 3v² - 12v + (5π - 10) = 0 derived from the area condition where the integral
    of y(t) x'(t) dt from 0 to 1 equals -π/4. Selects the smaller positive root for v. Then numerically computes
    the arc length L = ∫ sqrt((x'(t))² + (y'(t))²) dt from 0 to 1 using mpmath.quad.

    Complexity
    ----------
    O(1) as the numerical integration is performed with fixed precision requirements.

    References
    ----------
    https://projecteuler.net/problem=363
    """
    mp.dps = 20
    delta = sqrt(264 - 60 * pi)
    v = (12 - delta) / 6
    L = quad(lambda t: integrand(t, v), [0, 1])
    half_pi = pi / 2
    percent = 100 * (L - half_pi) / half_pi
    print('%.10f' % float(percent))

if __name__ == "__main__":
    main()