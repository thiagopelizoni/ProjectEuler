# Problem: https://projecteuler.net/problem=352
import numpy as np
import numba
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

@numba.njit
def compute_T(p, s):
    q = 1.0 - p
    powers = np.zeros(s + 1)
    powers[0] = 1.0
    for i in range(1, s + 1):
        powers[i] = powers[i - 1] * q
    u = np.zeros(s + 1)
    c = np.zeros(s + 1)
    for i in range(1, s + 1):
        if i == 1:
            u[1] = 1.0
            c[1] = 0.0
            continue

        min_c = np.inf
        denom = 1.0 - powers[i]
        for m in range(1, i): 
            pneg_c = powers[m] * (1.0 - powers[i - m]) / denom
            ppos_c = 1.0 - pneg_c
            cost = 1.0 + pneg_c * c[i - m] + ppos_c * (c[m] + u[i - m])
            if cost < min_c:
                min_c = cost
        c[i] = min_c

        min_u = np.inf
        for m in range(1, i + 1):
            pneg = powers[m]
            cost = 1.0 + pneg * u[i - m] + (1.0 - pneg) * (c[m] + u[i - m])
            if cost < min_u:
                min_u = cost
        u[i] = min_u
    return u[s]

def main():
    s = 10000
    ps = [0.01 * i for i in range(1, 51)]
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(compute_T, ps, [s] * len(ps)),
                            total=len(ps)))
    total = sum(results)
    print("{:.6f}".format(total))

if __name__ == "__main__":
    main()