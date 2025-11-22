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