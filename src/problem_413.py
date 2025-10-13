# Problem: https://projecteuler.net/problem=413
from collections import defaultdict
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def main():
    """
    Purpose
    -------
    Solve Project Euler problem 413 by computing F(10^19), the number of one-child numbers less than 10^19.

    Method / Math Rationale
    -----------------------
    For each digit length d from 1 to 19, use digit DP to count d-digit one-child numbers. The state tracks the capped
    number of bad substrings (0, 1, or 2+) and the frequency vector of suffix mods modulo d. When adding a digit, update
    the frequency vector by remapping the old frequencies according to the transition function and adding the new
    single-digit mod. The added bad substrings is the frequency of 0 in the new vector. To optimize, discard states
    where the number reaches 2 or more, as they cannot return to exactly 1. Aggregate ways for valid states.

    Complexity
    ----------
    O(sum_{d=1}^{19} d * 10 * d^2 * S_d) where S_d is the number of reachable frequency vectors for length d, expected
    to be manageable due to constraints and pruning.

    References
    ----------
    https://projecteuler.net/problem=413
    """
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(solve, range(1, 20)))
    total = sum(results)
    print(total)

def solve(d):
    m = d
    current = defaultdict(int)
    c = [0] * m
    key_c = tuple(c)
    key = (0, key_c)
    current[key] = 1
    for _ in tqdm(range(1, d + 1)):
        new_current = defaultdict(int)
        min_dgt = 1 if _ == 1 else 0
        for key, ways in current.items():
            zeros_cat, key_c = key
            c = list(key_c)
            for dgt in range(min_dgt, 10):
                new_c = [0] * m
                for s in range(m):
                    f = (s * 10 + dgt) % m
                    new_c[f] += c[s]
                new1 = dgt % m
                new_c[new1] += 1
                added = new_c[0]
                new_zeros_cat = min(2, zeros_cat + added)
                if new_zeros_cat < 2:
                    new_key_c = tuple(new_c)
                    new_key = (new_zeros_cat, new_key_c)
                    new_current[new_key] += ways
        current = new_current
    ans = 0
    for key, ways in current.items():
        zeros_cat, _ = key
        if zeros_cat == 1:
            ans += ways
    return ans

if __name__ == "__main__":
    main()