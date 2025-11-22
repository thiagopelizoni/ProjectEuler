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
    L = 10**7
    primes = list(primerange(2, L + 1))
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(compute_R, primes), total=len(primes)))
    total = sum(results)
    print(total)

if __name__ == "__main__":
    main()