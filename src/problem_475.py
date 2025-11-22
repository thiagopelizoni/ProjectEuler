# Problem: https://projecteuler.net/problem=475
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from math import comb
from tqdm import tqdm

MOD = 1000000007

def process_state(state_cnt, num_quartets):
    state, cnt = state_cnt
    n = list(state)  # [n0, n1, n2, n3, n4]
    local_next = defaultdict(int)

    # Case 1: three from same s
    for s in range(1, 5):
        if n[s] >= 3:
            ways = comb(n[s], 3) * (s ** 3) % MOD
            new_n = n[:]
            new_n[s] -= 3
            new_n[s - 1] += 3
            local_next[tuple(new_n)] = (local_next[tuple(new_n)] + cnt * ways % MOD) % MOD

    # Case 2: two from s, one from t != s
    for s in range(1, 5):
        if n[s] < 2:
            continue
        for t in range(1, 5):
            if t == s or n[t] < 1:
                continue
            ways = comb(n[s], 2) * n[t] * (s ** 2 * t) % MOD
            new_n = n[:]
            new_n[s] -= 2
            new_n[s - 1] += 2
            new_n[t] -= 1
            new_n[t - 1] += 1
            local_next[tuple(new_n)] = (local_next[tuple(new_n)] + cnt * ways % MOD) % MOD

    # Case 3: three different s > t > u
    for s in range(1, 5):
        if n[s] < 1:
            continue
        for t in range(1, s):
            if n[t] < 1:
                continue
            for u in range(1, t):
                if n[u] < 1:
                    continue
                ways = n[s] * n[t] * n[u] * (s * t * u) % MOD
                new_n = n[:]
                new_n[s] -= 1
                new_n[s - 1] += 1
                new_n[t] -= 1
                new_n[t - 1] += 1
                new_n[u] -= 1
                new_n[u - 1] += 1
                local_next[tuple(new_n)] = (local_next[tuple(new_n)] + cnt * ways % MOD) % MOD

    return local_next

def main():
    num_quartets = 150
    num_trios = 200
    initial_state = (0, 0, 0, 0, num_quartets)
    final_state = (num_quartets, 0, 0, 0, 0)

    current = {initial_state: 1}

    for _ in tqdm(range(num_trios)):
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(process_state, current.items(), [num_quartets] * len(current)))
        next_states = defaultdict(int)
        for res in results:
            for k, v in res.items():
                next_states[k] = (next_states[k] + v) % MOD
        current = next_states

    ways = current.get(final_state, 0)

    fact = 1
    for i in range(1, num_trios + 1):
        fact = fact * i % MOD

    inv_fact = pow(fact, MOD - 2, MOD)
    answer = ways * inv_fact % MOD

    print(answer)

if __name__ == "__main__":
    main()