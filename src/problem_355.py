# Problem: https://projecteuler.net/problem=355
from sympy import primerange
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import pulp


def find_for_p(p, n, primes_set, max_power_p, max_power):
    """Find candidate pairs for a given small prime p."""
    local_cand = []

    for q in primes_set:
        if q <= p:
            continue

        upper = n // q
        if upper < p:
            continue

        current = p
        while current <= upper // p:
            current *= p

        m = current * q
        max_q = q if q * q > n else max_power[q] if q in max_power else q

        if m > max_power_p + max_q:
            gain = m - max_power_p - max_q
            local_cand.append((gain, frozenset([p, q])))

    return local_cand


def main():
    """
    Purpose
    -------
    Solves Project Euler problem 355: Find the maximal possible sum of a set of mutually co-prime elements
    from {1, 2, ..., 200000}.

    Method / Math Rationale
    ---------------------
    Compute the base sum as 1 plus the sum of maximal prime powers p^k <= 200000 for each prime p. Improve this
    by identifying profitable combinations where a number m = p^a * q (with p < q primes) yields a gain
    m - (max_p + max_q) > 0. Model these as edges in a bipartite graph between small and large primes with
    weights as gains. Use integer linear programming to find the maximum weight matching, adding the total gain
    to the base sum.

    Complexity
    ----------
    - Time: O(S * Q * log_p N) for candidate generation (S ~90 small primes, Q ~18k primes, log ~20), plus ILP
      solving time (feasible for 30k variables).
    - Space: O(number of candidates) ~ O(30k).

    References
    ----------
    https://projecteuler.net/problem=355
    """
    n = 200000

    primes = list(primerange(2, n + 1))
    primes_set = set(primes)

    max_power = {}
    for p in primes:
        power = p
        while power * p <= n:
            power *= p
        max_power[p] = power

    base_sum = sum(max_power.values()) + 1

    small_primes = [p for p in primes if p * p <= n]
    candidates = []

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(find_for_p, p, n, primes_set, max_power[p], max_power)
            for p in small_primes
        ]
        for future in tqdm(futures, desc="Processing small primes"):
            candidates.extend(future.result())

    cand_id = range(len(candidates))
    all_small = set(small_primes)
    larges = set()
    for _, s in candidates:
        larges.update(s - all_small)

    small_to_cands = defaultdict(list)
    large_to_cands = defaultdict(list)
    gain_dict = {}

    for i in cand_id:
        g, s = candidates[i]
        gain_dict[i] = g
        ps = sorted(list(s))
        small = ps[0]
        large = ps[1]
        small_to_cands[small].append(i)
        large_to_cands[large].append(i)

    prob = pulp.LpProblem("Max_Gain", pulp.LpMaximize)
    x = {i: pulp.LpVariable(f"x_{i}", 0, 1, pulp.LpInteger) for i in cand_id}
    prob += pulp.lpSum(gain_dict[i] * x[i] for i in cand_id)

    for sm in small_to_cands:
        prob += pulp.lpSum(x[c] for c in small_to_cands[sm]) <= 1
    for lg in large_to_cands:
        prob += pulp.lpSum(x[c] for c in large_to_cands[lg]) <= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    total_gain = pulp.value(prob.objective)
    answer = base_sum + total_gain

    print(int(answer))


if __name__ == "__main__":
    main()