# Problem: https://projecteuler.net/problem=316
import sympy as sp
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def compute_g(n: int) -> int:
    s = [int(dig) for dig in str(n)]
    d = len(s)
    pi = [0] * d
    if d > 1:
        j = 0
        for i in range(1, d):
            while j > 0 and s[i] != s[j]:
                j = pi[j - 1]
            if s[i] == s[j]:
                j += 1
            pi[i] = j
    trans = [[0] * 10 for _ in range(d)]
    for state in range(d):
        for char in range(10):
            temp = state
            while temp > 0 and char != s[temp]:
                temp = pi[temp - 1]
            if char == s[temp]:
                trans[state][char] = temp + 1
            else:
                trans[state][char] = 0
    A = sp.eye(d) * 10
    for i in range(d):
        counts = [0] * d
        for c in range(10):
            ns = trans[i][c]
            if ns < d:
                counts[ns] += 1
        for j in range(d):
            A[i, j] -= counts[j]
    b = sp.Matrix(d, 1, [10] * d)
    E = A.solve(b)
    e0 = E[0, 0]
    g_val = e0 - d + 1
    return int(g_val)

def main():
    """
    Purpose
    Computes the sum of g(floor(10^16 / n)) for n=2 to 999999, where g(n) is the expected starting position of the
    first occurrence of n's digits in a random infinite decimal sequence.

    Method / Math Rationale
    The problem requires calculating a sum involving the function g(n), which is the expected starting index k for
    the digits of n to appear in a random digit sequence.
    To compute g(n), we convert n to its digit list s of length d.
    We use a Markov chain with states 0 to d-1 representing the matched prefix length.
    Transitions are built using the KMP prefix table to handle overlaps.
    We set up the system 10*E_i - sum (counts to j) * E_j = 10, solved exactly using sympy.Matrix.solve for the
    expected steps E_i.
    Then g(n) = E_0 - d + 1.
    To compute the sum efficiently, we collect counts of each unique floor(10^16 / n), compute g for uniques in
    parallel using ProcessPoolExecutor, and accumulate the weighted sum.

    Complexity
    O(MAX_N + U * d^3) where MAX_N=999999, U is number of unique m (~MAX_N), d<=16. Parallelism reduces wall time
    by number of CPUs.

    References
    https://projecteuler.net/problem=316
    """
    N = 10**16
    MAX_N = 999999
    m_counts = Counter()
    for n in tqdm(range(2, MAX_N + 1), desc="Collecting m"):
        m = N // n
        m_counts[m] += 1
    unique_ms = list(m_counts.keys())
    g_values = {}
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(compute_g, m): m for m in unique_ms}
        for future in tqdm(as_completed(futures), total=len(unique_ms), desc="Computing g"):
            m = futures[future]
            g = future.result()
            g_values[m] = g
    total = 0
    for m, count in m_counts.items():
        total += count * g_values[m]
    print(total)

if __name__ == "__main__":
    main()