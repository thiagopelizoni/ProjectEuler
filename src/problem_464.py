# Problem: https://projecteuler.net/problem=464
import numpy as np
from numba import njit
from tqdm import tqdm

@njit
def add(fen, pos, val):
    while pos < len(fen):
        fen[pos] += val
        pos += pos & -pos

@njit
def query(fen, pos):
    s = 0
    while pos > 0:
        s += fen[pos]
        pos -= pos & -pos
    return s

@njit
def process_sorted(sorted_indices, m, V, shift, fen, ans):
    for idx in sorted_indices:
        cv = V[idx] + shift
        if idx <= m:
            add(fen, cv, 1)
        else:
            count = query(fen, cv)
            ans[idx] += count

def get_mobius(n):
    mu = np.zeros(n + 1, dtype=np.int8)
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    mu[1] = 1
    primes = []
    for i in tqdm(range(2, n + 1)):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def main():
    """
    Purpose
    -------
    Computes the number of integer pairs (a, b) with 1 <= a <= b <= 20000000 such that
    99 * N(a, b) <= 100 * P(a, b) and 99 * P(a, b) <= 100 * N(a, b), where P(a, b)
    and N(a, b) are the counts of numbers in [a, b] with Mobius function values 1 and
    -1, respectively. No parameters. Prints the result.

    Method / Math Rationale
    -----------------------
    Computes the Mobius function values up to n using a linear sieve. Constructs prefix
    sum arrays U and V where U corresponds to 100 * P - 99 * N and V to 100 * N - 99 * P.
    Reformulates the problem as counting, for each b, the number of j < b such that
    U[j] <= U[b] and V[j] <= V[b] using prefix sums. Employs CDQ divide-and-conquer to
    efficiently count these 2D dominated points by sorting on one dimension and using
    a Fenwick tree (binary indexed tree) on the shifted values of the other dimension.

    Complexity
    ----------
    O(n log^2 n) time, O(n) memory.

    References
    ----------
    https://projecteuler.net/problem=464
    """
    n = 20000000
    mu = get_mobius(n)
    U = np.zeros(n + 1, dtype=np.int64)
    V = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        U[i] = U[i - 1]
        V[i] = V[i - 1]
        if mu[i] == 1:
            U[i] += 100
            V[i] -= 99
        elif mu[i] == -1:
            U[i] -= 99
            V[i] += 100
    min_v = np.min(V)
    max_v = np.max(V)
    shift = -min_v + 1
    size = max_v - min_v + 2
    ans = np.zeros(n + 1, dtype=np.int64)

    def cdq(l, r):
        if l >= r:
            return
        m = (l + r) // 2
        cdq(l, m)
        cdq(m + 1, r)
        temp = np.arange(l, r + 1)
        sort_order = np.argsort(U[temp], kind='stable')
        sorted_temp = temp[sort_order]
        fen = np.zeros(size, dtype=np.int64)
        process_sorted(sorted_temp, m, V, shift, fen, ans)

    cdq(0, n)
    total = np.sum(ans[1:])
    print(total)

if __name__ == "__main__":
    main()