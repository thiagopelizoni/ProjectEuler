# Problem: https://projecteuler.net/problem=307
from decimal import Decimal, getcontext
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

def compute_term(l, n, k, log_fact, log_n, ln_two):
    getcontext().prec = 30
    start = n - k + l + 1
    log_prod = Decimal(0)
    for i in range(start, n + 1):
        log_prod += Decimal(i).ln()
    log_term = Decimal(l) * (-ln_two) + log_prod - log_fact[k - 2 * l] - log_fact[l] + log_fact[k] - Decimal(k) * log_n
    return log_term.exp()

def main():
    """
    Purpose
    Solves Project Euler problem 307: computes p(20000, 1000000), the probability that at least one chip has at least 3 defects.

    Method / Math Rationale
    Computes the complement probability that all chips have at most 2 defects as the sum over l (number of chips with exactly 2 defects) of
    (1/2)^l * n! / (n - k + l)! / (k - 2l)! / l! * k! / n^k using logarithmic computations for precision and incremental products implicitly
    through independent per-term calculations.

    Complexity
    O(k) for precomputations; O(k/2) for main loop with parallel term computations.

    References
    https://projecteuler.net/problem=307
    """
    getcontext().prec = 30
    n = 1000000
    k = 20000
    log_n = Decimal(n).ln()
    ln_two = Decimal(2).ln()
    log_fact = [Decimal(0) for _ in range(k + 1)]
    for i in range(1, k + 1):
        log_fact[i] = log_fact[i - 1] + Decimal(i).ln()
    max_l = k // 2
    num_workers = os.cpu_count()
    sum_prob = Decimal(0)
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(compute_term, l, n, k, log_fact, log_n, ln_two) for l in range(max_l + 1)]
        for future in tqdm(as_completed(futures), total=len(futures)):
            sum_prob += future.result()
    prob_at_least_one = Decimal(1) - sum_prob
    print('{:.10f}'.format(prob_at_least_one.quantize(Decimal('1e-10'))))

if __name__ == "__main__":
    main()