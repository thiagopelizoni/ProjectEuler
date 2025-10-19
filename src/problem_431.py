# Problem: https://projecteuler.net/problem=431
import numpy as np
from math import pi, tan
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ellipe
from tqdm import tqdm

def integrand(rho, x):
    if rho == 0:
        return 0.0
    sr = np.sqrt(x * rho)
    denom = x + rho
    k = 2 * sr / denom
    E = ellipe(k**2)
    return 4 * rho * (x + rho) * E

def compute_I(x, r):
    return quad(integrand, 0, r, args=(x,), epsabs=1e-12, epsrel=1e-12)[0]

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 431 by computing the sum of all x values where the wasted space V(x) is a perfect square.

    Method / Math Rationale
    -----------------------
    The wasted space V(x) = tan(alpha) * \iint_D sqrt((a - x)^2 + b^2) da db over the disk D of radius r.
    This integral I(x) is computed as 4 \int_0^r \rho (x + \rho) E( (2 sqrt(x \rho) / (x + \rho))^2 ) d\rho,
    where E is the complete elliptic integral of the second kind.
    For each integer n from 20 to 25, solve I(x) = n^2 / tan(alpha) using Brent's method to find x,
    then sum these x values.

    Complexity
    ----------
    O(1) effectively, as the number of n is fixed at 6, each requiring a fixed number of integral evaluations.

    References
    ----------
    https://projecteuler.net/problem=431
    """
    r = 6.0
    alpha = 40 * pi / 180
    tan_alpha = tan(alpha)
    sum_x = 0.0
    for n in tqdm(range(20, 26)):
        target = n**2 / tan_alpha
        x = brentq(lambda xv: compute_I(xv, r) - target, 0, r, rtol=1e-12)
        sum_x += x
    print(f"{sum_x:.9f}")

if __name__ == "__main__":
    main()