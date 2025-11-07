# Problem: https://projecteuler.net/problem=481
from fractions import Fraction
from itertools import combinations
from math import comb
from tqdm import tqdm

def get_next(mask, curr):
    for k in range(curr + 1, 15):
        if mask & (1 << (k - 1)):
            return k
    for k in range(1, 15):
        if mask & (1 << (k - 1)):
            return k

def masks_with_pop(n_bits, pop):
    for combi in combinations(range(n_bits), pop):
        yield sum(1 << i for i in combi)

def solve_linear_multi(A, bs):
    n = len(A)
    m = len(bs)
    M = [A[i][:] + [bs[k][i] for k in range(m)] for i in range(n)]
    for i in range(n):
        if M[i][i] == Fraction(0):
            for j in range(i + 1, n):
                if M[j][i] != Fraction(0):
                    M[i], M[j] = M[j], M[i]
                    break
            else:
                raise ValueError("Singular matrix")
        pivot = M[i][i]
        for c in range(i, n + m):
            M[i][c] /= pivot
        for j in range(i + 1, n):
            factor = M[j][i]
            for c in range(i, n + m):
                M[j][c] -= factor * M[i][c]
    x = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(n - 1, -1, -1):
        for k in range(m):
            x[k][i] = M[i][n + k]
            for j in range(i + 1, n):
                x[k][i] -= M[i][j] * x[k][j]
    return x

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 481: compute the expected number of dishes cooked in a competition
    with 14 chefs.

    Method / Math Rationale
    -----------------------
    Uses bottom-up dynamic programming over subsets (masks) of chefs, ordered by increasing size.
    For each subset, solves linear systems of equations to compute expected values and win
    probabilities for each starting chef, handling cyclic dependencies via Gaussian elimination
    on fractions.
    Players choose eliminations optimally to maximize their win probability, with ties broken by
    eliminating the chef with the next-closest turn in the cycle.

    Complexity
    ----------
    O(2^n n^3) time for DP and linear system solves using Gaussian elimination.
    For n=14, feasible.

    References
    ----------
    https://projecteuler.net/problem=481
    """
    fib = [0] * 16
    fib[1] = fib[2] = 1
    for i in range(3, 16):
        fib[i] = fib[i - 1] + fib[i - 2]
    S = [None] + [Fraction(fib[k], fib[15]) for k in range(1, 15)]
    exp_dict = {}
    wins_dict = {}
    for pop in range(1, 15):
        for mask in tqdm(masks_with_pop(14, pop), total=comb(14, pop), desc=f"Pop {pop}"):
            rem = sorted([i for i in range(1, 15) if mask & (1 << (i - 1))])
            k = len(rem)
            if k == 1:
                c = rem[0]
                exp_dict[(mask, c)] = Fraction(0)
                wins = [Fraction(0)] * 15
                wins[c] = Fraction(1)
                wins_dict[(mask, c)] = wins
                continue
            chosen_es = [None] * k
            chosen_succ_exps = [None] * k
            chosen_succ_winss = [None] * k
            for start_idx in range(k):
                curr = rem[start_idx]
                order = [rem[(start_idx + off) % k] for off in range(1, k)]
                candidates = []
                for e in order:
                    new_mask = mask & ~(1 << (e - 1))
                    new_next = get_next(new_mask, curr)
                    succ_exp = exp_dict[(new_mask, new_next)]
                    succ_wins = wins_dict[(new_mask, new_next)]
                    my_win = succ_wins[curr]
                    candidates.append((my_win, e, succ_exp, succ_wins))
                max_win = max(c[0] for c in candidates)
                for my_win, e, succ_exp, succ_wins in candidates:
                    if my_win == max_win:
                        chosen_es[start_idx] = e
                        chosen_succ_exps[start_idx] = succ_exp
                        chosen_succ_winss[start_idx] = succ_wins
                        break
            A = [[Fraction(0) for _ in range(k)] for _ in range(k)]
            b_exp = [Fraction(0) for _ in range(k)]
            for start_idx in range(k):
                curr = rem[start_idx]
                p = S[curr]
                next_idx = (start_idx + 1) % k
                A[start_idx][start_idx] = Fraction(1)
                A[start_idx][next_idx] = p - Fraction(1)
                b_exp[start_idx] = Fraction(1) + p * chosen_succ_exps[start_idx]
            bs = [b_exp]
            for jj_idx, jj in enumerate(rem):
                b_win = [Fraction(0) for _ in range(k)]
                for start_idx in range(k):
                    p = S[rem[start_idx]]
                    e = chosen_es[start_idx]
                    succ_wins = chosen_succ_winss[start_idx]
                    add = Fraction(0) if jj == e else succ_wins[jj]
                    b_win[start_idx] = p * add
                bs.append(b_win)
            solutions = solve_linear_multi(A, bs)
            exp_list = solutions[0]
            wins_sols = solutions[1:]
            for start_idx in range(k):
                curr = rem[start_idx]
                key = (mask, curr)
                exp_dict[key] = exp_list[start_idx]
                wins = [Fraction(0) for _ in range(15)]
                for jj_idx, jj in enumerate(rem):
                    wins[jj] = wins_sols[jj_idx][start_idx]
                wins_dict[key] = wins
    mask = (1 << 14) - 1
    exp = exp_dict[(mask, 1)]
    print(f"{float(exp):.8f}")

if __name__ == "__main__":
    main()