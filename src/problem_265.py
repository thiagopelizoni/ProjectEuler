# Problem: https://projecteuler.net/problem=265
from tqdm import tqdm

def backtrack(s, current_mask, used, pos, n, mask_n, mask_nm1, pbar):
    pbar.update(1)
    if pos == (1 << n):
        for k in range(1, n):
            wrap_bits = s[-(n - k):] + s[:k]
            wrap_int = 0
            for bit in wrap_bits:
                wrap_int = (wrap_int << 1) | bit
            if used[wrap_int]:
                return 0
        num = 0
        for bit in s:
            num = (num << 1) | bit
        return num
    total = 0
    for b in range(2):
        new_sub = (current_mask << 1 | b) & mask_n
        if not used[new_sub]:
            used[new_sub] = True
            new_current_mask = new_sub & mask_nm1
            s.append(b)
            total += backtrack(s, new_current_mask, used, pos + 1, n, mask_n, mask_nm1, pbar)
            s.pop()
            used[new_sub] = False
    return total

n = 5
length = 1 << n
mask_n = (1 << n) - 1
mask_nm1 = (1 << (n - 1)) - 1
s = [0] * n
used = [False] * length
used[0] = True
current_mask = 0
pos = n
pbar = tqdm(desc="Backtracking steps")
sum_s = backtrack(s, current_mask, used, pos, n, mask_n, mask_nm1, pbar)
pbar.close()
print(sum_s)