# Problem: https://projecteuler.net/problem=259
import os
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from tqdm import tqdm
from typing import List, Set, Tuple

def compute_subexpression_values(
    args: Tuple[Set[Fraction], Set[Fraction]]
) -> Set[Fraction]:
    left_values, right_values = args
    results = set()
    for left in left_values:
        for right in right_values:
            results.add(left + right)
            results.add(left - right)
            results.add(left * right)
            if right != 0:
                results.add(left / right)
    return results

def get_cpu_count() -> int:
    try:
        return os.cpu_count() or 1
    except (NotImplementedError, AttributeError):
        return 1

def main() -> None:
    digits = "123456789"
    n = len(digits)
    reachable_values: List[List[Set[Fraction]]] = [
        [set() for _ in range(n)] for _ in range(n)
    ]
    for i in range(n):
        for j in range(i, n):
            num_str = digits[i : j + 1]
            value = Fraction(int(num_str))
            reachable_values[i][j].add(value)
    cpu_count = get_cpu_count()
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        pbar = tqdm(range(2, n + 1), desc="Calculating reachable numbers")
        for length in pbar:
            task_args: List[Tuple[Set[Fraction], Set[Fraction]]] = []
            task_meta: List[Tuple[int, int]] = []
            for start in range(n - length + 1):
                end = start + length - 1
                for split in range(start, end):
                    left_vals = reachable_values[start][split]
                    right_vals = reachable_values[split + 1][end]
                    task_args.append((left_vals, right_vals))
                    task_meta.append((start, end))
            if task_args:
                results = executor.map(compute_subexpression_values, task_args)
                for idx, combos in enumerate(results):
                    start, end = task_meta[idx]
                    reachable_values[start][end].update(combos)
    all_values = reachable_values[0][n - 1]
    total = 0
    for val in all_values:
        if val > 0 and val.denominator == 1:
            total += val.numerator
    print(total)

if __name__ == "__main__":
    main()