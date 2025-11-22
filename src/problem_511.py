# Problem: https://projecteuler.net/problem=511
import numpy as np
from numba import njit
from tqdm import tqdm
from itertools import product

def main():
    n = 1234567898765
    k = 4321
    MOD = 1000000000

    primes = [5, 41, 25343, 237631]
    combos = product(*[[1, p] for p in primes])
    D = [np.prod(combo) for combo in combos]

    freq = np.zeros(k, dtype=np.int64)
    for d in D:
        res = d % k
        freq[res] += 1

    r = (k - (n % k)) % k

    @njit
    def circular_convolution(a, b, mod):
        kk = a.shape[0]
        res = np.zeros(kk, dtype=np.int64)
        for i in range(kk):
            for j in range(kk):
                idx = (i + j) % kk
                prod = (a[i] * b[j]) % mod
                res[idx] = (res[idx] + prod) % mod
        return res

    def poly_pow(base, exp, mod):
        kk = base.shape[0]
        result = np.zeros(kk, dtype=np.int64)
        result[0] = 1
        bits = bin(exp)[2:]
        pbar = tqdm(total=len(bits), desc="Polynomial exponentiation")
        for i in range(len(bits)):
            bit = bits[-1 - i]
            if bit == '1':
                result = circular_convolution(result, base, mod)
            base = circular_convolution(base, base, mod)
            pbar.update(1)
        pbar.close()
        return result

    powered = poly_pow(freq, n, MOD)
    answer = powered[r]
    print(answer)

if __name__ == "__main__":
    main()