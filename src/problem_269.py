# Problem: https://projecteuler.net/problem=269
import gc
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from typing import Dict, Tuple

def compute_count(mask: int, length: int) -> int:
    S = [i + 1 for i in range(9) if mask & (1 << i)]
    sign = (-1) ** len(S)
    if not S:
        return sign * 9 * 10 ** (length - 1)
    ks = S
    m = len(ks)
    memo: Dict[Tuple[int, ...], int] = {}
    zero_tuple = tuple(0 for _ in ks)
    memo[zero_tuple] = 1
    for pos in range(length):
        next_memo: Dict[Tuple[int, ...], int] = {}
        min_d = 1 if pos == 0 else 0
        max_d = 9
        for s_tuple, ways in memo.items():
            for d in range(min_d, max_d + 1):
                good = True
                new_s_list = []
                for j in range(m):
                    k = ks[j]
                    s = s_tuple[j]
                    if (s - d) % k != 0:
                        good = False
                        break
                    new_s = - (s - d) // k
                    new_s_list.append(new_s)
                if good:
                    new_tuple = tuple(new_s_list)
                    next_memo.setdefault(new_tuple, 0)
                    next_memo[new_tuple] += ways
        memo = next_memo
    count = memo.get(zero_tuple, 0)
    return sign * count

def main() -> None:
    length = 16
    total = 10 ** length - 1
    no_roots = 0
    with ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:
        futures = [
            executor.submit(compute_count, mask, length)
            for mask in range(1 << 9)
        ]
        for future in tqdm(as_completed(futures), total=1 << 9):
            no_roots += future.result()
            gc.collect()
    z = total - no_roots + 1
    print(z)

if __name__ == "__main__":
    main()