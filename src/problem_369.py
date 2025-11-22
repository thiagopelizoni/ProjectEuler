# Problem: https://projecteuler.net/problem=369
from math import comb as C
from functools import reduce
import operator

cs = {
    0b0001: 1, 0b0010: 1, 0b0100: 1, 0b1000: 1,
    0b0011: 2, 0b0101: 2, 0b0110: 2, 0b1001: 2, 0b1010: 2, 0b1100: 2,
    0b0111: 3, 0b1011: 3, 0b1101: 3, 0b1110: 3,
    0b1111: 4
}

vs = tuple(cs.keys())

def count(s):
    p, n = 1, 13
    for i in set(s):
        k = s.count(i)
        p *= C(n, k)
        n -= k
    return p

def badugi(s):
    n = len(s)
    if n < 4: return False
    if reduce(operator.or_, s, 0) != 0b1111: return False
    for a in range(n):
        if s[a] & 0b0001 == 0: continue
        for b in range(n):
            if b == a or s[b] & 0b0010 == 0: continue
            for c in range(n):
                if c in (a, b) or s[c] & 0b0100 == 0: continue
                for d in range(n):
                    if d in (a, b, c) or s[d] & 0b1000 == 0: continue
                    return True
    return False

def solve(n, m, s, p, b):
    if not b and n > 3: b = badugi(s)
    if n == m:
        return count(s) if b else 0
    if len(s) == 13: return 0
    t = 0
    for q in range(p, len(vs)):
        v = vs[q]
        if n + cs[v] > m: continue
        t += solve(n + cs[v], m, s + [v], q, b)
    return t

def main():
    total = 0
    for i in range(4, 14):
        total += solve(0, i, [], 0, False)
    print(total)

if __name__ == "__main__":
    main()