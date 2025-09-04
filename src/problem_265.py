# Problem: https://projecteuler.net/problem=265
from tqdm import tqdm

def backtrack(binary_sequence: list[int], current_suffix_mask: int, substring_used: list[bool],
              current_position: int, n: int, full_mask: int, suffix_mask: int, pbar: tqdm) -> int:
    pbar.update(1)
    if current_position == (1 << n):
        for k in range(1, n):
            wrap_bits = binary_sequence[-(n - k):] + binary_sequence[:k]
            wrap_int = 0
            for bit in wrap_bits:
                wrap_int = (wrap_int << 1) | bit
            if substring_used[wrap_int]:
                return 0
        num = 0
        for bit in binary_sequence:
            num = (num << 1) | bit
        return num
    total = 0
    for b in range(2):
        new_sub = ((current_suffix_mask << 1) | b) & full_mask
        if not substring_used[new_sub]:
            substring_used[new_sub] = True
            new_suffix_mask = new_sub & suffix_mask
            binary_sequence.append(b)
            total += backtrack(binary_sequence, new_suffix_mask, substring_used, current_position + 1,
                               n, full_mask, suffix_mask, pbar)
            binary_sequence.pop()
            substring_used[new_sub] = False
    return total

def main() -> None:
    """
    Purpose: Solves Project Euler problem 265, computing the sum of all 2^5-bit binary numbers starting with 5 zeros
    such that the circular arrangement has all unique 5-bit substrings.

    Args: None

    Returns: None; the computed sum is printed to standard output.

    Method / Math Rationale: Employs backtracking to extend the binary sequence from an initial string of N zeros,
    ensuring each new N-bit substring is unique by tracking usage. This simulates traversing unused edges in the
    de Bruijn graph for binary strings of length N. Upon reaching full length 2^N, verifies the N-1 wrapping
    substrings do not conflict with used ones, ensuring the circle covers all 2^N unique substrings via pigeonhole
    principle, as 2^N - (N - 1) linear substrings are already distinct.

    Complexity: Time O(2^{2^N / 2}) worst-case due to backtracking with pruning (feasible for N=5); space O(2^N)
    for tracking used substrings and the sequence.

    References: https://projecteuler.net/problem=265
    de Bruijn sequences and Eulerian cycles in directed graphs.
    """
    n = 5
    sequence_length = 1 << n
    full_mask = (1 << n) - 1
    suffix_mask = (1 << (n - 1)) - 1
    binary_sequence = [0] * n
    substring_used = [False] * sequence_length
    substring_used[0] = True
    current_suffix_mask = 0
    current_position = n
    pbar = tqdm(desc="Backtracking steps")
    total_sum = backtrack(binary_sequence, current_suffix_mask, substring_used, current_position, n, full_mask,
                          suffix_mask, pbar)
    pbar.close()
    print(total_sum)

if __name__ == "__main__":
    main()