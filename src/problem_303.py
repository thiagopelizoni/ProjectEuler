# Problem: https://projecteuler.net/problem=303
import concurrent.futures
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def compute_k(n):
    seen = set()
    queue = deque()
    parent = {}
    for start_d in [1, 2]:
        r = start_d % n
        if r not in seen:
            seen.add(r)
            queue.append(r)
            parent[r] = (-1, start_d)
            if r == 0:
                return start_d // n
    while queue:
        current_r = queue.popleft()
        for d in range(3):
            new_r = (current_r * 10 + d) % n
            if new_r == 0:
                digits = [str(d)]
                rem = current_r
                while rem != -1:
                    prev, dig = parent[rem]
                    digits.append(str(dig))
                    rem = prev
                m_str = ''.join(digits[::-1])
                m = int(m_str)
                return m // n
            if new_r not in seen:
                seen.add(new_r)
                queue.append(new_r)
                parent[new_r] = (current_r, d)

def main():
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(compute_k, n) for n in range(1, 10001)]
    total = 0
    for future in tqdm(as_completed(futures), total=10000):
        total += future.result()
    print(total)

if __name__ == "__main__":
    main()