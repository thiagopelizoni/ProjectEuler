# Problem: https://projecteuler.net/problem=525
import numpy as np
from numba import njit, prange

@njit(fastmath=True, cache=True)
def elliptical_arc_length(a, b, n_steps):
    dt = (np.pi / 2.0) / n_steps
    total = 0.0
    for i in prange(n_steps):
        t = (i + 0.5) * dt
        st2 = np.sin(t) ** 2
        ct2 = np.cos(t) ** 2
        r = np.sqrt(a * a * ct2 + b * b * st2)
        jac = (a * b) / (b * b * ct2 + a * a * st2)
        total += r * jac
    return 4.0 * total * dt

def main():
    ITERATIONS = 50_000_000
    c1 = elliptical_arc_length(1.0, 4.0, ITERATIONS)
    c3 = elliptical_arc_length(3.0, 4.0, ITERATIONS)
    print(f"{c1 + c3:.8f}")

if __name__ == "__main__":
    main()