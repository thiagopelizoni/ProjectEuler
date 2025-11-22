# Problem: https://projecteuler.net/problem=413
from collections import defaultdict
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def main():
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