# Problem: https://projecteuler.net/problem=367
from collections import defaultdict, Counter
from itertools import combinations, permutations
from math import factorial
import numpy as np
from sympy.utilities.iterables import partitions
from tqdm import tqdm

def get_representative(cycle_lengths):
    n = sum(cycle_lengths)
    perm = list(range(n))
    pos = 0
    for length in cycle_lengths:
        for i in range(length - 1):
            perm[pos + i] = pos + i + 1
        if length > 0:
            perm[pos + length - 1] = pos
        pos += length
    return perm

def get_cycle_type(perm):
    n = len(perm)
    visited = [False] * n
    cycles = []
    for start in range(n):
        if not visited[start]:
            length = 0
            x = start
            while not visited[x]:
                visited[x] = True
                x = perm[x]
                length += 1
            cycles.append(length)
    return tuple(sorted(cycles, reverse=True))

def class_size(n, part):
    m = Counter(part)
    z = 1
    for l, ml in m.items():
        z *= (l ** ml) * factorial(ml)
    return factorial(n) // z

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 367 by computing the expected number of shuffles
    in the described Bozo sort variant for n=11, averaged over all permutations,
    and prints the rounded value.

    Method / Math Rationale
    -----------------------
    Models the problem as a Markov chain on the symmetric group S_11, grouping
    states by cycle types (partitions of 11). Computes transition probabilities
    between cycle types by simulating all possible 3-element shuffles on
    representative permutations. Solves the system of linear equations for
    expected values using numpy.linalg.solve. Averages using class sizes and
    rounds to nearest integer.

    Complexity
    ----------
    O(p * C(n,3) * 6 * n) where p is number of partitions (~56 for n=11), due
    to simulating shuffles and computing cycle types; solving O(p^3). Overall
    negligible for n=11.

    References
    ----------
    https://projecteuler.net/problem=367
    """
    n = 11
    parts = [tuple(sorted(sum([[k]*v for k,v in p.items()], []), reverse=True)) for p in partitions(n)]
    id_part = (1,) * n
    num_classes = len(parts)
    part_to_idx = {part: i for i, part in enumerate(parts)}
    id_idx = part_to_idx[id_part]
    transient = [i for i in range(num_classes) if i != id_idx]
    num_trans = len(transient)
    m = len(list(combinations(range(n), 3))) * 6

    part_to_prob = {}
    for part in tqdm(parts):
        rep = get_representative(list(part))
        count = defaultdict(int)
        for comb in combinations(range(n), 3):
            pos = list(comb)
            for rho in permutations(range(3)):
                new_perm = rep[:]
                for k in range(3):
                    old_pos = pos[rho[k]]
                    new_perm[pos[k]] = rep[old_pos]
                mu = get_cycle_type(new_perm)
                count[mu] += 1
        part_to_prob[part] = {mu: c / m for mu, c in count.items()}

    A = np.eye(num_trans)
    b = np.ones(num_trans)
    for row in range(num_trans):
        k = transient[row]
        part = parts[k]
        probs = part_to_prob[part]
        for mu, p in probs.items():
            if mu == id_part:
                continue
            l = part_to_idx[mu]
            col = transient.index(l)
            A[row, col] -= p

    E_trans = np.linalg.solve(A, b)
    full_E = np.zeros(num_classes)
    for i in range(num_trans):
        full_E[transient[i]] = E_trans[i]
    full_E[id_idx] = 0

    fact_n = factorial(n)
    total = 0.0
    for i, part in enumerate(parts):
        total += full_E[i] * class_size(n, part)
    avg = total / fact_n
    print(round(avg))

if __name__ == "__main__":
    main()