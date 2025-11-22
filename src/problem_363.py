# Problem: https://projecteuler.net/problem=363
from mpmath import mp, quad, sqrt, pi

def dxdt(t, v):
    return (6 * v - 6) * t + (6 - 9 * v) * t**2

def dydt(t, v):
    return 3 * v + (6 - 12 * v) * t + (9 * v - 6) * t**2

def integrand(t, v):
    return sqrt(dxdt(t, v)**2 + dydt(t, v)**2)

def main():
    mp.dps = 20
    delta = sqrt(264 - 60 * pi)
    v = (12 - delta) / 6
    L = quad(lambda t: integrand(t, v), [0, 1])
    half_pi = pi / 2
    percent = 100 * (L - half_pi) / half_pi
    print('%.10f' % float(percent))

if __name__ == "__main__":
    main()