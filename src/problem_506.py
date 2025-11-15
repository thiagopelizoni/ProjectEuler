# Problem: https://projecteuler.net/problem=506

from math import gcd


def mod_inverse(a, m):
    return pow(a, -1, m)


def geom_sum(QQ, M, base, inv_basem1):
    if QQ == 0:
        return 0
    pow_b_QQ = pow(base, QQ, M)
    return (base * (pow_b_QQ - 1) * inv_basem1) % M


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 506 by computing S(10^14) mod 123454321, where S(n) is the sum of the first n
    terms in the clock sequence.

    Method / Math Rationale
    -----------------------
    The digit sequence is 1 followed by repeating "234321". We model the consumption of digits for each v_k using
    modular arithmetic over the period 6. The state transitions cycle every 15 steps starting from k=2. We group
    computations into cycles of 15, using closed-form geometric series sums for efficient calculation of large
    exponents modulo M.

    Complexity
    ----------
    O(1) effectively, with logarithmic operations for modular exponentiations.

    References
    ----------
    https://projecteuler.net/problem=506
    """
    N = 10**14
    M = 123454321

    cycle = [2, 3, 4, 3, 2, 1]
    s_to_rem = [{0: 0} for _ in range(6)]
    prefix_s = [[0] * 6 for _ in range(6)]

    for r in range(6):
        cum = 0
        for remm in range(1, 6):
            cum += cycle[(r + remm - 1) % 6]
            prefix_s[r][remm] = cum
            s_to_rem[r][cum] = remm

    p_num = [[0] * 6 for _ in range(6)]
    for r in range(6):
        cur = 0
        for remm in range(1, 6):
            cur = cur * 10 + cycle[(r + remm - 1) % 6]
            p_num[r][remm] = cur

    C = [0] * 6
    for r in range(6):
        rot = cycle[r:] + cycle[:r]
        C[r] = int(''.join(map(str, rot)))

    ten6 = pow(10, 6, M)
    ten6m1 = (ten6 - 1) % M
    inv_ten6m1 = mod_inverse(ten6m1, M)

    positions = []
    cr = 0
    for kk in range(2, 17):
        s = kk % 15
        rem = s_to_rem[cr][s]
        positions.append((cr, rem))
        cr = (cr + rem) % 6

    As = [0] * 15
    Bs = [0] * 15
    ps = [0] * 15
    rems = [0] * 15

    for idx, (r, rem) in enumerate(positions):
        p = p_num[r][rem]
        crv = C[r]
        ten_rem = pow(10, rem, M)
        temp = crv * inv_ten6m1 % M
        A = temp * ten_rem % M
        B = (p - temp * ten_rem % M) % M
        As[idx] = A
        Bs[idx] = B
        ps[idx] = p
        rems[idx] = rem

    S = 1 % M
    num_steps = N - 1
    num_cycles = num_steps // 15
    remain = num_steps % 15

    base = ten6
    basem1 = (base - 1) % M
    inv_basem1 = mod_inverse(basem1, M)

    for j in range(15):
        A = As[j]
        B = Bs[j]
        p = ps[j]
        if j < 13:
            Q = num_cycles
            if Q == 0:
                sum_this = 0
            elif Q == 1:
                sum_this = p % M
            else:
                geom = geom_sum(Q - 1, M, base, inv_basem1)
                sum_this = (p + A * geom + B * (Q - 1)) % M
        else:
            Q = num_cycles
            if Q == 0:
                sum_this = 0
            else:
                geom = geom_sum(Q, M, base, inv_basem1)
                sum_this = (A * geom + B * Q) % M
        S = (S + sum_this) % M

    if remain > 0:
        next_m = num_cycles + 1
        for rr in range(remain):
            j = rr
            if j < 13:
                qq = next_m - 1
            else:
                qq = next_m
            r = positions[j][0]
            rem = rems[j]
            p = ps[j]
            if qq == 0:
                v = p % M
            else:
                ten6q = pow(ten6, qq, M)
                sum_geom = (ten6q - 1) * inv_ten6m1 % M
                full = C[r] * sum_geom % M
                ten_rem = pow(10, rem, M)
                v = (full * ten_rem + p) % M
            S = (S + v) % M

    print(S)


if __name__ == "__main__":
    main()