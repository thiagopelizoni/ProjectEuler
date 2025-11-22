# Problem: https://projecteuler.net/problem=306
from tqdm import tqdm

def main():
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