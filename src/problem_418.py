# Problem: https://projecteuler.net/problem=418
from mpmath import mp, mpf, log, exp
from tqdm import tqdm
import bisect

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
candidates = {}

def factorize_factorial(limit):
    factors = [0] * len(primes)
    for i in range(2, limit + 1):
        reduce = i
        for j, p in enumerate(primes):
            while reduce % p == 0:
                factors[j] += 1
                reduce //= p
    return factors

def find_candidates(max_exps, pos, current, current_exps, at_least, at_most):
    if pos == len(primes):
        if current >= at_least and current <= at_most:
            candidates[current] = current_exps[:]
        return
    max_exponent = max_exps[pos]
    temp_current = current
    for e in range(max_exponent + 1):
        current_exps[pos] = e
        if temp_current > at_most:
            break
        find_candidates(max_exps, pos + 1, temp_current, current_exps, at_least, at_most)
        if e < max_exponent:
            if temp_current * primes[pos] > at_most:
                break
            temp_current *= primes[pos]

def search(root3, factors):
    if not candidates:
        return 0
    cand_list = sorted(candidates.items())
    keys = [val for val, _ in cand_list]
    mid_idx = bisect.bisect_left(keys, root3)
    best_num = cand_list[-1][0]
    best_den = cand_list[0][0]
    result = 0
    a_list = cand_list[:mid_idx]
    c_list = cand_list[mid_idx:]
    for a_idx in tqdm(range(len(a_list) - 1, -1, -1)):
        a, a_exps = a_list[a_idx]
        for c_idx in range(len(c_list)):
            c, c_exps = c_list[c_idx]
            if c * best_den >= best_num * a:
                break
            is_valid = True
            b = 1
            for k in range(len(primes)):
                used = a_exps[k] + c_exps[k]
                if used > factors[k]:
                    is_valid = False
                    break
                remain = factors[k] - used
                b *= primes[k] ** remain
            if not is_valid:
                continue
            if b < a or b > c:
                continue
            if c * best_den <= best_num * a:
                best_num = c
                best_den = a
                result = a + b + c
                break
    return result

def main():
    """
    Purpose
    -------
    Compute f(43!) as defined in Project Euler problem 418, which is the sum a + b + c 
    for the unique factorization triple (a, b, c) of 43! with 1 <= a <= b <= c and 
    a * b * c = 43! that minimizes c / a.
    No parameters.
    Prints the sum a + b + c.
    
    Method / Math Rationale
    -----------------------
    Factorize 43! into its prime exponents. Approximate the cube root of 43! using 
    high-precision logarithms. Generate all divisors within a narrow range around 
    the cube root using recursive enumeration with pruning. For each pair of 
    candidates a below and c above the cube root, compute b from remaining 
    exponents, validate the triple, and track the one with minimal c / a using 
    exact integer comparisons to avoid floating-point precision issues.
    
    Complexity
    ----------
    Generating candidates: Recursive over 14 primes, pruned to ~1000 candidates 
    by tight bounds, effectively O(1) for fixed input.
    Searching: O(number of candidates^2) in worst case, but early termination 
    reduces it significantly; for ~1000 candidates, feasible.
    
    References
    ----------
    https://projecteuler.net/problem=418
    """
    limit = 43
    delta = 0.0002
    mp.dps = 100
    logn = mp.zero
    for i in range(2, limit + 1):
        logn += log(mpf(i))
    root_mp = exp(logn / 3)
    root3 = float(root_mp)
    at_least = float(root_mp * mpf(1 - delta / 2))
    at_most = float(root_mp * mpf(1 + delta / 2))
    factors = factorize_factorial(limit)
    current_exps = [0] * len(primes)
    find_candidates(factors, 0, 1, current_exps, at_least, at_most)
    sum_abc = search(root3, factors)
    print(sum_abc)

if __name__ == "__main__":
    main()