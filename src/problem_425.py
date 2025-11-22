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