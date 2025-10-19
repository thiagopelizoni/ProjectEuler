# Problem: https://projecteuler.net/problem=430
from decimal import Decimal, getcontext
from tqdm import tqdm

def main():
    """
    Purpose
    -------
    Solves Project Euler problem 430, computing the expected number of white disks after 4000 flips for 10^10 disks.

    Method / Math Rationale
    -----------------------
    E(N, M) = N/2 + (1/2) * sum_{i=1}^N (1 - 2*p_i)^M where p_i = (2*i*(N - i +1) -1) / N^2 is the probability disk i is flipped in one turn.
    1 - 2*p_i = (4*i**2 - 4*(N+1)*i + N**2 +2) / N**2
    Due to symmetry r_i = 1-2*p_i = r_{N+1-i}, and for large i the terms are zero for practical purposes, compute sum for i=1 to K where term <=1e-10, double it.

    Complexity
    ----------
    O(K) time where K ≈ N / (4*M) ≈ 6.25e5, but in practice around 1e7 for precision.

    References
    ----------
    https://projecteuler.net/problem=430
    """
    getcontext().prec = 50
    N = 10000000000
    M = 4000
    DN = Decimal(N)
    DNN = DN ** 2
    s = Decimal(0)
    max_k = 20000000
    for i in tqdm(range(1, max_k + 1)):
        Di = Decimal(i)
        num = 4 * Di ** 2 - 4 * (DN + 1) * Di + DN ** 2 + Decimal(2)
        r = num / DNN
        term = r ** M
        if term < Decimal('1e-12'):
            break
        s += term

    total = 2 * s
    E = DN / 2 + Decimal('0.5') * total
    print('{:.2f}'.format(float(E)))

if __name__ == "__main__":
    main()