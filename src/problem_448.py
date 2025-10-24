# Problem: https://projecteuler.net/problem=448
import math
from tqdm import tqdm


def main():
    """
    Purpose
    -------
    Solve Project Euler problem 448 by computing S(n) mod 999999017 where n=99999999019.

    Method / Math Rationale
    ------------------------
    A(k) = sum_{i=1}^k i / gcd(k,i)
    S(n) = 1/2 * n + 1/2 * sum_{d=1}^n V(floor(n/d)) where V(m) = sum_{k=1}^m k * phi(k)
    Use Min_25 sieve to compute V(m) for all needed floor(n/d).
    The function f(k) = k * phi(k) is multiplicative with f(p^e) = p^{2e} - p^{2e-1}.
    Compute sum over primes using sieving, then add higher power contributions using recurrence.

    Complexity
    ----------
    O(n^{3/4} / log n)

    References
    ----------
    https://projecteuler.net/problem=448
    """
    n = 99999999019
    MOD = 999999017
    inv2 = pow(2, MOD - 2, MOD)

    sqrtn = math.isqrt(n) + 10
    Q = [n // i for i in range(1, sqrtn + 1) if n // i != 0]
    Q += list(range(Q[-1] - 1, 0, -1))
    Q = sorted(set(Q), reverse=True)

    S0 = {x: (x - 1) % MOD for x in Q}
    S1 = {x: (x * (x + 1) * inv2 % MOD - 1 + MOD) % MOD for x in Q}
    S2 = {x: x * (x + 1) % MOD * (2 * x + 1) % MOD * pow(6, MOD - 2, MOD) % MOD for x in Q}

    ps = []
    sieve = [True] * (sqrtn + 1)
    for x in range(2, sqrtn + 1):
        if sieve[x]:
            ps.append(x)
            for multiple in range(x * 2, sqrtn + 1, x):
                sieve[multiple] = False

    for x in ps:
        px = x % MOD
        px2 = px * px % MOD
        for nn in Q:
            if nn < x * x:
                break
            np = nn // x
            diff0 = (S0[np] - S0[x - 1] + MOD) % MOD
            diff1 = (S1[np] - S1[x - 1] + MOD) % MOD
            diff2 = (S2[np] - S2[x - 1] + MOD) % MOD
            S0[nn] = (S0[nn] - diff0 + MOD) % MOD
            S1[nn] = (S1[nn] - px * diff1 % MOD + MOD) % MOD
            S2[nn] = (S2[nn] - px2 * diff2 % MOD + MOD) % MOD

    Fprime = {x: (S2[x] - 1 - S1[x] + 2 * MOD) % MOD for x in Q}

    def func(p, e):
        pe = pow(p, e, MOD)
        p2e = pe * pe % MOD
        p2em1 = p2e * pow(p, MOD - 2, MOD) % MOD
        return (p2e - p2em1 + MOD) % MOD

    f = {x: Fprime[x] for x in Q}
    f[0] = 0

    for p in tqdm(reversed(ps)):
        delta = {}
        for nn in Q:
            if nn < p * p:
                continue
            pc = p
            c = 1
            contrib = 0
            while nn // pc >= p:
                npc = nn // pc
                temp = (f.get(npc, 0) - Fprime.get(p, 0) + MOD) % MOD
                contrib = (contrib + func(p, c) * temp % MOD) % MOD
                contrib = (contrib + func(p, c + 1)) % MOD
                c += 1
                pc *= p
            delta[nn] = contrib
        for nn in delta:
            f[nn] = (f[nn] + delta[nn]) % MOD

    for x in Q:
        f[x] = (f[x] + 1) % MOD

    W = 0
    i = 1
    while i <= n:
        q = n // i
        r = n // q
        num = r - i + 1
        W = (W + num * f.get(q, 0) % MOD) % MOD
        i = r + 1

    result = (n % MOD * inv2 % MOD + W * inv2 % MOD) % MOD
    print(result)


if __name__ == "__main__":
    main()