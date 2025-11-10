# Problem: https://projecteuler.net/problem=490
import sympy
from sympy import S
from tqdm import tqdm

def mod(x, m):
    return (x % m + m) % m

def main():
    """
    Purpose
    Solve Project Euler problem 490: compute S(10^14) mod 10^9 where S(L) = sum_{n=1}^L f(n)^3 and f(n) is the number of ways the frog can visit all stones 1 to n exactly once, ending at n, with jumps of at most 3 units.

    Method / Math Rationale
    Use full bitmask DP to compute f(n) for n=1 to 20. Find the linear recurrence for f(n) by solving systems with sympy. Extend the state to include sum of cubes and monomials up to degree 3 for matrix exponentiation to compute the sum up to L=10^14 mod 10^9.

    Complexity
    Bitmask DP: O(20 * 2^20 * 6) ~ 10^8 operations. Finding recurrence: O(10^3) small. Matrix power: O(166^3 log 10^14) ~ 2e8 operations.

    References
    https://projecteuler.net/problem=490
    """

    MOD = 10**9
    max_n = 20
    f = [0] * (max_n + 1)
    for N in tqdm(range(1, max_n + 1)):
        full = (1 << N) - 1
        dp = [[0] * (N + 1) for _ in range(1 << N)]
        dp[1][1] = 1
        for mask in range(1 << N):
            for pos in range(1, N + 1):
                if dp[mask][pos] == 0:
                    continue
                bit = pos - 1
                if (mask & (1 << bit)) == 0:
                    continue
                for delta in [-3, -2, -1, 1, 2, 3]:
                    p = pos + delta
                    if 1 <= p <= N and (mask & (1 << (p - 1))) == 0:
                        new_mask = mask | (1 << (p - 1))
                        dp[new_mask][p] += dp[mask][pos]
        f[N] = dp[full][N]

    assert f[6] == 14
    assert f[10] == 254
    s10 = sum(f[i]**3 for i in range(1, 11))
    assert s10 == 18230635

    # Find recurrence
    d = None
    coeffs = None
    for possible_d in range(1, 21):
        rows = []
        for i in range(possible_d):
            row = [f[possible_d + i +1 -j] for j in range(1, possible_d +1)]
            rows.append(row)
        A = sympy.Matrix(rows)
        b = sympy.Matrix([f[possible_d +1 +i] for i in range(possible_d)])
        try:
            a = A.solve(b)
            if all(isinstance(ai, sympy.Integer) for ai in a):
                valid = True
                for nn in range(possible_d + possible_d +1, max_n +1):
                    predicted = sum(int(a[k]) * f[nn -k -1] for k in range(possible_d))
                    if predicted != f[nn]:
                        valid = False
                        break
                if valid:
                    d = possible_d
                    coeffs = [int(ai) for ai in a]
                    break
        except:
            pass
    assert d is not None

    # Extend to 40 to verify
    ff = f[:]
    for nn in range(max_n + 1, 41):
        predicted = sum(coeffs[k] * ff[nn -1 -k] for k in range(d))
        ff.append(predicted)
    assert ff[40] == 1439682432976

    monos = []
    def gen_exponents(curr, pos, remaining, d):
        if pos == d:
            if remaining == 0:
                monos.append(tuple(curr[:]))
            return
        for e in range(remaining + 1):
            curr[pos] = e
            gen_exponents(curr, pos + 1, remaining - e, d)
    gen_exponents([0] * d, 0, 0, d)
    gen_exponents([0] * d, 0, 1, d)
    gen_exponents([0] * d, 0, 2, d)
    gen_exponents([0] * d, 0, 3, d)
    monos.sort(key=lambda e: (sum(e), e))

    dim_monos = len(monos)
    dim = dim_monos + 1  # + S

    # sympy symbols
    x = [sympy.symbols(f'x{k}') for k in range(d)]

    f_next = sum(coeffs[k] * x[k] for k in range(d))

    # Build the matrix
    mat = [[0 for _ in range(dim)] for _ in range(dim)]

    # For S row (index 0)
    s_next = f_next ** 3
    expanded = s_next.expand()
    terms = expanded.as_coefficients_dict()
    for term, coeff in terms.items():
        exp = [0] * d
        if term != 1:
            powers = term.as_powers_dict()
            for varr, poww in powers.items():
                idx = int(str(varr)[1:])
                exp[idx] = poww
        exp_tuple = tuple(exp)
        idx = monos.index(exp_tuple) + 1
        mat[0][idx] = mod(int(coeff), MOD)
    mat[0][0] = 1

    # For each mono row
    for mm in range(dim_monos):
        e = list(monos[mm])
        mono_next = S(1)
        for ii in range(d):
            if e[ii] > 0:
                base = f_next if ii == 0 else x[ii - 1]
                mono_next *= base ** e[ii]
        expanded = mono_next.expand()
        terms = expanded.as_coefficients_dict()
        for term, coeff in terms.items():
            exp = [0] * d
            if term != 1:
                powers = term.as_powers_dict()
                for varr, poww in powers.items():
                    idx = int(str(varr)[1:])
                    exp[idx] = poww
            exp_tuple = tuple(exp)
            idx = monos.index(exp_tuple) + 1
            mat[mm + 1][idx] = mod(int(coeff), MOD)

    # Initial at n = d
    init_vec = [0] * dim
    init_vec[0] = mod(sum(f[i]**3 for i in range(1, d + 1)), MOD)
    for mm in range(dim_monos):
        e = monos[mm]
        val = 1
        for ii in range(d):
            if e[ii] > 0:
                val *= f[d - ii] ** e[ii]
        init_vec[mm + 1] = mod(val, MOD)

    # Matrix power M ^ (L - d) * init_vec mod MOD
    L = 10**14
    if L < d:
        result = mod(sum(f[i]**3 for i in range(1, L + 1)), MOD)
    else:
        exp = L - d
        powered = matrix_power(mat, exp, MOD)
        result_vec = matrix_vector_mul(powered, init_vec, MOD)
        result = result_vec[0]

    print(result)

def matrix_mul(a, b, mod):
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % mod
    return c

def matrix_power(m, exp, mod):
    n = len(m)
    res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while exp > 0:
        if exp % 2 == 1:
            res = matrix_mul(res, m, mod)
        m = matrix_mul(m, m, mod)
        exp //= 2
    return res

def matrix_vector_mul(m, v, mod):
    n = len(v)
    res = [0] * n
    for i in range(n):
        for j in range(n):
            res[i] = (res[i] + m[i][j] * v[j]) % mod
    return res

if __name__ == "__main__":
    main()