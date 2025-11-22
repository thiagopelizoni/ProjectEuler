# Problem: https://projecteuler.net/problem=414
from math import factorial
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def get_multinoms():
    """Precompute multinomial coefficients for digit group sizes."""
    multinoms = []
    for mask in range(16):
        current_size = 1
        groups = []
        for i in range(4):
            if mask & (1 << i):
                current_size += 1
            else:
                groups.append(current_size)
                current_size = 1
        groups.append(current_size)
        prod_fact = 1
        for sz in groups:
            prod_fact *= factorial(sz)
        multinom = 120 // prod_fact
        multinoms.append(multinom)
    return multinoms

MULTINOMS = get_multinoms()

def compute_S(b):
    """Compute S(b) for a given base b."""
    t = (b - 3) // 6
    a_cb = 4 * t + 2
    c_cb = 2 * t + 1
    succ_a = [[0] * b for _ in range(b)]
    succ_c = [[0] * b for _ in range(b)]
    for a in range(b):
        for c in range(b):
            if a == 0 and c == 0:
                continue
            d0 = b - a
            d1 = b - c - 1
            d2 = b - 1
            d3 = c - 1 if c >= 1 else b - 1
            d4 = a if c >= 1 else a - 1 if a >= 1 else b - 1
            digs = [d0, d1, d2, d3, d4]
            s = sorted(digs)
            new_a = s[4] - s[0]
            new_c = s[3] - s[1]
            succ_a[a][c] = new_a
            succ_c[a][c] = new_c
    depth = [[-1] * b for _ in range(b)]
    depth[a_cb][c_cb] = 0
    for aa in range(b):
        for cc in range(b):
            if aa == 0 and cc == 0:
                continue
            if depth[aa][cc] != -1:
                continue
            chain = []
            curr_a, curr_c = aa, cc
            seen = set()
            while curr_a < b and curr_c < b and depth[curr_a][curr_c] == -1:
                key = curr_a * b + curr_c
                if key in seen:
                    for prev_a, prev_c in chain:
                        depth[prev_a][prev_c] = -2  # Mark cycle
                    break
                seen.add(key)
                chain.append((curr_a, curr_c))
                next_a = succ_a[curr_a][curr_c]
                next_c = succ_c[curr_a][curr_c]
                curr_a, curr_c = next_a, next_c
            else:
                if curr_a >= b or curr_c >= b:
                    for prev_a, prev_c in chain:
                        depth[prev_a][prev_c] = -2  # Mark invalid
                    continue
                d = depth[curr_a][curr_c]
                for prev_a, prev_c in reversed(chain):
                    d += 1
                    depth[prev_a][prev_c] = d
    sum_part = 0
    for a in tqdm(range(b), desc=f"Base {b}"):
        for c in range(b):
            if a == 0 and c == 0:
                continue
            if depth[a][c] == -2 or a < c:
                num = 0
            else:
                diff = a - c
                num = 0
                for mask in range(16):
                    min_g = 0
                    max_g = diff
                    if mask & 1:
                        min_g = max_g = 0
                    else:
                        min_g = max(min_g, 1)
                    if mask & 8:
                        min_g = max(min_g, diff)
                        max_g = min(max_g, diff)
                    else:
                        max_g = min(max_g, diff - 1)
                    n_g1 = max(0, max_g - min_g + 1)
                    min_d = 0
                    max_d = c
                    if mask & 2:
                        min_d = max_d = 0
                    else:
                        min_d = max(min_d, 1)
                    if mask & 4:
                        min_d = max(min_d, c)
                        max_d = min(max_d, c)
                    else:
                        max_d = min(max_d, c - 1)
                    n_delta = max(0, max_d - min_d + 1)
                    num += (b - a) * n_g1 * n_delta * MULTINOMS[mask]
            sum_part += depth[a][c] * num if depth[a][c] >= 0 else 0
    total_non_all_minus1 = pow(b, 5) - b - 1
    return total_non_all_minus1 + sum_part

def main():
    bs = [6 * k + 3 for k in range(2, 301)]
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_S, bs))
    total = sum(results)
    last_18 = f"{total % (10**18):018d}"
    print(last_18)

if __name__ == "__main__":
    main()