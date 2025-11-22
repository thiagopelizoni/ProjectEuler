# Problem: https://projecteuler.net/problem=470
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import bicgstab

def compute_R(S, c):
    if not S:
        return 0.0

    k = len(S)
    if c == 0:
        return float(max(S))

    mu = sum(S) / k
    e_prev = mu
    best = max(0.0, mu - c)
    t = 1
    while True:
        t += 1
        s_max = sum(max(v, e_prev) for v in S)
        e_curr = s_max / k
        marg = e_curr - e_prev
        if marg <= c:
            break

        net = e_curr - c * t
        if net > best:
            best = net

        e_prev = e_curr
        if t > 1000:
            break

    return best

def compute_for_c(params):
    d, c, active, M, full_mask = params
    size = 1 << d
    N = size - 1
    reward = np.zeros(N)
    for mask in range(1, size):
        i = mask - 1
        reward[i] = compute_R(active[mask], c)

    value_vec, info = bicgstab(M, reward, rtol=1e-12)
    if info != 0:
        raise ValueError("Solver did not converge")

    return value_vec[full_mask - 1]

def main():
    total = 0.0
    for d in range(4, 21):
        size = 1 << d
        N = size - 1
        full_mask = size - 1
        active = [[] for _ in range(size)]
        for mask in range(1, size):
            for i in range(d):
                if mask & (1 << i):
                    active[mask].append(i + 1)

        M = lil_matrix((N, N))
        for mask in tqdm(range(1, size)):
            row = mask - 1
            M[row, row] = 1.0
            for f in range(d):
                new_mask = mask ^ (1 << f)
                if new_mask != 0:
                    col = new_mask - 1
                    M[row, col] -= 1.0 / d

        M = M.tocsr()
        params_list = [(d, c, active, M, full_mask) for c in range(21)]
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(compute_for_c, params_list))
        total += sum(results)

    print(round(total))

if __name__ == "__main__":
    main()