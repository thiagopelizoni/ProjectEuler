# Problem: https://projecteuler.net/problem=321
from typing import List

def generate_sequence(start1: int, start2: int, max_terms: int = 30) -> List[int]:
    seq = [start1, start2]
    while len(seq) < max_terms:
        next_val = 6 * seq[-1] - seq[-2]
        seq.append(next_val)
    return seq

def main():
    ls_chain1 = generate_sequence(1, 4)
    ls_chain2 = generate_sequence(2, 11)
    all_ns = sorted([l - 1 for l in ls_chain1 + ls_chain2 if l - 1 >= 1])
    sum_first_40 = sum(all_ns[:40])
    print(sum_first_40)

if __name__ == "__main__":
    main()