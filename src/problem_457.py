# Problem: https://projecteuler.net/problem=457
from concurrent.futures import ProcessPoolExecutor
from sympy.ntheory.generate import primerange
from sympy.ntheory import sqrt_mod
from tqdm import tqdm

def compute_R(p):
    s = sqrt_mod(13, p)
    if s is None:
        return 0
    mod_p2 = p * p
    k = (s * s - 13) // p
    try:
        inv_2s = pow(2 * s, -1, p)
    except ValueError:
        return 0
    t = (-k * inv_2s) % p
    S = (s + t * p) % mod_p2
    inv2 = pow(2, -1, mod_p2)
    n1 = ((3 + S) * inv2) % mod_p2
    n2 = ((3 - S) * inv2) % mod_p2
    return min(n1, n2)

def main():
    """
    Purpose
    -------
    Compute and print SR(10^7), the sum of R(p) for all primes p <= 10^7, where R(p) is the smallest
    positive integer n such that n^2 - 3n - 1 ≡ 0 mod p^2, or 0 if no such n exists.

    Method / Math Rationale
    -----------------------
    For each prime p, if 13 is not a quadratic residue modulo p, R(p) = 0. Otherwise, compute the
    square root of 13 modulo p and lift it to modulo p^2 using Hensel's lemma. Then, use the quadratic
    formula modulo p^2 to find the two solutions n1 and n2, and set R(p) to the minimum of them.
    Cases where lifting fails (e.g., p=2, p=13) are handled by checking invertibility.

    Complexity
    ----------
    O(π(10^7) * log^2(10^7)), parallelized over available CPUs.

    References
    ----------
    https://projecteuler.net/problem=457
    """
    L = 10**7
    primes = list(primerange(2, L + 1))
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(compute_R, primes), total=len(primes)))
    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()