# Problem: https://projecteuler.net/problem=268
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from tqdm import tqdm
from sympy.ntheory import primerange

def compute_partial(primes, start_idx, init_prod, init_omega, M):
    """
    Computes the partial contributions to T[j] starting from a given index, product, and omega.
    
    Args:
    primes (list): List of primes less than 100.
    start_idx (int): Starting index in the primes list.
    init_prod (int): Initial product.
    init_omega (int): Initial omega.
    M (int): The upper limit (10**16).
    
    Returns:
    list: Partial T[j] contributions.
    """
    partial_t = [0] * 26
    
    def rec(current_prod, idx, omega):
        if idx == len(primes):
            partial_t[omega] += (M - 1) // current_prod
            return
        rec(current_prod, idx + 1, omega)
        new_prod = current_prod * primes[idx]
        if new_prod <= M - 1:
            rec(new_prod, idx + 1, omega + 1)
    
    rec(init_prod, start_idx, init_omega)
    return partial_t

def solve():
    """
    Solves Project Euler problem 268: Count the number of positive integers less than 10^16 
    that are divisible by at least four distinct primes less than 100.
    
    The solution uses binomial inversion on the count of numbers with exactly m distinct 
    small prime factors. We compute T_j as the sum over all products of exactly j distinct 
    primes p < 100 of floor((10^16 - 1) / prod). Then, for m = 0 to 3, compute the counts 
    S(m) of numbers with exactly m such factors using the inversion formula 
    S(m) = sum_{j >= m} (-1)^{j-m} * binom(j, m) * T_j. The desired count is then 
    (10^16 - 1) - sum_{m=0}^3 S(m).
    
    This approach was derived by recognizing the problem as counting integers with at least 
    4 distinct small prime factors, using inclusion-exclusion via binomial transform inversion 
    for efficiency, and generating the necessary sums via recursive enumeration of prime products 
    with pruning for performance.
    
    Returns:
    int: The count of such numbers.
    """
    M = 10**16
    primes = list(primerange(2, 100))
    num_split = 5
    t = [0] * 26
    tasks = []
    with ProcessPoolExecutor() as executor:
        for bits in product([0, 1], repeat=num_split):
            init_prod = 1
            init_omega = 0
            overflow = False
            for bit_idx, include in enumerate(bits):
                if include:
                    next_prod = init_prod * primes[bit_idx]
                    if next_prod > M - 1:
                        overflow = True
                        break
                    init_prod = next_prod
                    init_omega += 1
            if not overflow:
                future = executor.submit(
                    compute_partial, primes, num_split, init_prod, init_omega, M
                )
                tasks.append(future)
        for future in tqdm(as_completed(tasks), total=len(tasks)):
            partial_t = future.result()
            for j in range(26):
                t[j] += partial_t[j]
    at_most_3 = 0
    for m in range(4):
        s_m = 0
        for j in range(m, 26):
            sign = 1 if (j - m) % 2 == 0 else -1
            s_m += sign * math.comb(j, m) * t[j]
        at_most_3 += s_m
    return (M - 1) - at_most_3

if __name__ == "__main__":
    print(solve())