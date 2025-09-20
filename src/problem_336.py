# Problem: https://projecteuler.net/problem=336
import string
from math import factorial
from tqdm import tqdm

def next_perm(arr):
    n = len(arr)
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1:] = arr[i + 1:][::-1]
    return True

def main():
    """
    Purpose
    -------
    Solve Project Euler Problem 336: find the 2011th lexicographic maximix arrangement for 11 carriages.

    Method / Math Rationale
    -----------------------
    Generate permutations in lexicographic order starting from the smallest possible candidate ('CABDEFGHIJK'). For each, simulate Simple Simon's
    rearrangement process and check if it requires the maximum number of rotations (2*(n-1)-1 =19 for n=11). Count such arrangements until
    reaching the 2011th.

    Complexity
    ----------
    Time: O((n-1)! * n^2) in worst case, but with early exits.
    Space: O(n)

    References
    ----------
    https://projecteuler.net/problem=336
    """
    n = 11
    letters = string.ascii_uppercase[:n]
    first_start = 'C'
    rest = [c for c in letters if c != first_start]
    rest.sort()
    current_perm = list(first_start + ''.join(rest))
    total_perms = (ord(letters[-1]) - ord(first_start) + 1) * factorial(n - 1)
    with tqdm(total=total_perms) as pbar:
        count = 0
        target = 2011
        while True:
            work = current_perm[:]
            breaked = False
            for i in range(n - 1):
                expect = letters[i]
                last = n - 1
                if work[i] == expect or (work[last] == expect and i != n - 2):
                    breaked = True
                    break
                j = i
                while work[j] != expect:
                    j += 1
                if j < last:
                    work[j:last + 1] = work[j:last + 1][::-1]
                work[i:last + 1] = work[i:last + 1][::-1]
            if not breaked:
                count += 1
                if count == target:
                    print(''.join(current_perm))
                    break
            if not next_perm(current_perm):
                break
            pbar.update(1)

if __name__ == "__main__":
    main()