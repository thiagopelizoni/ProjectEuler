# Problem: https://projecteuler.net/problem=469
from decimal import Decimal, getcontext

def main():
    """
    Purpose
    -------
    Computes E(10^18), the expected fraction of empty chairs for N=10^18 chairs,
    as described in the problem.

    Method / Math Rationale
    ------------------------
    For large N, E(N) approaches (1 + exp(-2))/2, derived from the infinite-volume
    limit of the random sequential adsorption process on 1D lattice with
    nearest-neighbor exclusion. The process models the knight seating.

    Complexity
    ----------
    O(1), constant time computation.

    References
    ----------
    https://projecteuler.net/problem=469
    https://arxiv.org/abs/2210.05627
    """
    getcontext().prec = 30
    exp_minus_2 = Decimal('-2').exp()
    e_n = (Decimal(1) + exp_minus_2) / Decimal(2)
    rounded = e_n.quantize(Decimal('1e-14'))
    print(f"{rounded:f}")

if __name__ == "__main__":
    main()