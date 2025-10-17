# Problem: https://projecteuler.net/problem=425
import sympy.ntheory as nt
from collections import defaultdict
from tqdm import tqdm

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            if self.rank[px] < self.rank[py]:
                self.parent[px] = py
            elif self.rank[px] > self.rank[py]:
                self.parent[py] = px
            else:
                self.parent[py] = px
                self.rank[px] += 1

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 425: compute F(10^7), the sum of primes <= 10^7
    that are not 2's relatives.
    Parameters: None
    Returns: None (prints the result)

    Method / Math Rationale
    -----------------------
    Generate all primes up to N=10^7 using sympy.ntheory.generate.primerange.
    Use a Union-Find structure to connect primes incrementally in increasing order.
    For each prime P, connect it to the prime Q obtained by removing its first digit
    if Q is prime and the remaining string does not start with '0' (to ensure exactly
    one digit added without leading zeros), and to same-length primes differing in
    exactly one digit using bucketing by masked strings for each position.
    After making connections, check if P is in the same component as 2; if not,
    add P to the sum of non-relatives.
    This ensures connectivity in the subgraph of primes <= P.

    Complexity
    ----------
    Time: O(P * D * alpha(P)), where P is the number of primes (~664k), D is max
    digits (7), and alpha is the inverse Ackermann function (~constant).
    Space: O(P * D) for buckets and Union-Find.

    References
    ----------
    https://projecteuler.net/problem=425
    """
    N = 10**7
    primes = list(nt.generate.primerange(2, N + 1))
    num_primes = len(primes)
    prime_to_idx = {primes[i]: i for i in range(num_primes)}
    uf = UnionFind(num_primes)
    idx_2 = prime_to_idx[2]
    max_d = 7
    buckets = [None] * (max_d + 1)
    for d in range(1, max_d + 1):
        buckets[d] = [defaultdict(list) for _ in range(d)]
    non_rel_sum = 0
    for idx in tqdm(range(num_primes)):
        p = primes[idx]
        strp = str(p)
        d = len(strp)
        if d >= 2:
            q_str = strp[1:]
            if q_str[0] != '0':
                q = int(q_str)
                if q in prime_to_idx:
                    uf.union(idx, prime_to_idx[q])
        for i in range(d):
            mask = strp[:i] + '*' + strp[i+1:]
            for prev_idx in buckets[d][i][mask]:
                uf.union(idx, prev_idx)
        if uf.find(idx) != uf.find(idx_2):
            non_rel_sum += p
        for i in range(d):
            mask = strp[:i] + '*' + strp[i+1:]
            buckets[d][i][mask].append(idx)
    print(non_rel_sum)

if __name__ == "__main__":
    main()