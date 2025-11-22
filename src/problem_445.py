# Problem: https://projecteuler.net/problem=445
from math import isqrt
from tqdm import tqdm
from numba import jit, prange

@jit
def s_p(m, p):
    s = 0
    while m > 0:
        m //= p
        s += m
    return s

def get_primes(n):
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, isqrt(n) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

class SegmentTree:
    def __init__(self, n, mod):
        self.n = n
        self.mod = mod
        self.tree = [0] * (4 * (n + 1))
        self.lazy = [1] * (4 * (n + 1))

    def push(self, node, start, end):
        if self.lazy[node] != 1:
            self.tree[node] = (self.tree[node] * self.lazy[node]) % self.mod
            if start != end:
                self.lazy[2 * node] = (self.lazy[2 * node] * self.lazy[node]) % self.mod
                self.lazy[2 * node + 1] = (self.lazy[2 * node + 1] * self.lazy[node]) % self.mod
            self.lazy[node] = 1

    def update(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if start > end or start > r or end < l:
            return
        if l <= start and end <= r:
            self.lazy[node] = (self.lazy[node] * val) % self.mod
            self.push(node, start, end)
            return
        mid = (start + end) // 2
        self.update(2 * node, start, mid, l, r, val)
        self.update(2 * node + 1, mid + 1, end, l, r, val)
        self.tree[node] = (self.tree[2 * node] + self.tree[2 * node + 1]) % self.mod

    def build(self, node, start, end, values):
        if start == end:
            self.tree[node] = values[start] % self.mod
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid, values)
        self.build(2 * node + 1, mid + 1, end, values)
        self.tree[node] = (self.tree[2 * node] + self.tree[2 * node + 1]) % self.mod

    def get_sum(self):
        self.push(1, 0, self.n)
        return self.tree[1]

def main():
    N = 10000000
    MOD = 1000000007
    B = isqrt(N)

    primes = get_primes(N)
    small_primes = [p for p in primes if p <= B]
    large_primes = [p for p in primes if p > B]

    s_N_p = {}
    for p in small_primes:
        s_N_p[p] = s_p(N, p)

    f_small = [0] * (N + 1)
    for k in tqdm(range(1, N)):
        prod = 1
        for p in small_primes:
            v = s_N_p[p] - s_p(k, p) - s_p(N - k, p)
            if v > 0:
                pv = pow(p, v, MOD)
                prod = (prod * (1 + pv)) % MOD
        f_small[k] = prod

    st = SegmentTree(N, MOD)
    values = [0] * (N + 1)
    for k in range(1, N):
        values[k] = f_small[k]

    st.build(1, 0, N, values)

    for p in tqdm(large_primes):
        val = (1 + p) % MOD
        a = (N % p) + 1
        j_max = N // p
        for j in range(j_max + 1):
            start = j * p + a
            end = min(j * p + p - 1, N)
            if start <= end:
                st.update(1, 0, N, start, end, val)

    sum_F = st.get_sum()
    two_N = pow(2, N, MOD)
    result = (sum_F - (two_N - 2) % MOD + MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()