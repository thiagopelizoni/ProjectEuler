# Problem: https://projecteuler.net/problem=306
from tqdm import tqdm

def main():
    """
    Purpose
    Solves Project Euler problem 306: counts the number of n from 1 to 1,000,000 where the first player can force a win in the paper-strip game.

    Method / Math Rationale
    The game is Dawson's Kayles, where Grundy numbers determine winning positions (g(n) != 0 for first-player win).
    Compute Grundy numbers up to a point where periodicity of 34 is observed starting from n=70.
    Count non-zero g(n) in initial segment (1-69), then in full periods of 34, and remainder.

    Complexity
    O(M^2) where M ~ 100 for precomputing Grundy numbers, constant time overall.

    References
    https://projecteuler.net/problem=306
    """
    MAX_N = 1000000
    M = 103
    g = [0] * (M + 1)

    for k in tqdm(range(M + 1)):
        s = set()
        for i in range(1, k):
            s.add(g[i - 1] ^ g[k - i - 1])
        mex = 0
        while mex in s:
            mex += 1
        g[k] = mex

    initial_end = 69
    initial_wins = sum(1 for i in range(1, initial_end + 1) if g[i] != 0)
    cycle = g[70:104]
    cycle_size = len(cycle)
    cycle_wins = sum(1 for x in cycle if x != 0)
    remaining = MAX_N - initial_end
    num_cycles = remaining // cycle_size
    rem = remaining % cycle_size
    periodic_wins = num_cycles * cycle_wins
    rem_wins = sum(1 for i in range(rem) if cycle[i] != 0)
    total_wins = initial_wins + periodic_wins + rem_wins
    print(total_wins)

if __name__ == "__main__":
    main()