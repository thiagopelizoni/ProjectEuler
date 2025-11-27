# Problem: https://projecteuler.net/problem=534
import numpy as np
from numba import njit, prange
from tqdm import tqdm

@njit(fastmath=True, cache=True)
def check_conflict_backtrack(current_row, col, history, limit):
    start = current_row - 1
    stop = current_row - limit - 1
    if stop < -1: stop = -1
    
    for r in range(start, stop, -1):
        prev_col = history[r]
        diff = current_row - r
        
        if prev_col == col:
            return True
        d = prev_col - col
        if d == diff or d == -diff:
            return True
            
    return False

@njit(fastmath=True, cache=True)
def solve_recursive(row, n, limit, history):
    if row == n:
        return 1
    
    count = 0
    for c in range(n):
        if not check_conflict_backtrack(row, c, history, limit):
            history[row] = c
            count += solve_recursive(row + 1, n, limit, history)
    return count

@njit(parallel=True, fastmath=True, cache=True)
def run_backtracking(n, limit):
    total = 0
    for c0 in prange(n):
        history = np.empty(n, dtype=np.int32)
        history[0] = c0
        total += solve_recursive(1, n, limit, history)
    return total

@njit(fastmath=True, cache=True)
def get_initial_count(idx, n, R):
    cols = np.empty(R, dtype=np.int32)
    temp = idx
    for k in range(R - 1, -1, -1):
        cols[k] = temp % n
        temp //= n
        
    for i in range(R):
        for j in range(i + 1, R):
            c1 = cols[i]
            c2 = cols[j]
            dist = j - i
            if c1 == c2: 
                return 0
            d = c1 - c2
            if d == dist or d == -dist: 
                return 0
    return 1

@njit(fastmath=True, cache=True)
def compute_transition_kernel(idx, n, R, prev_counts, high_multiplier):
    h = np.empty(R, dtype=np.int32)
    temp = idx
    for k in range(R - 1, -1, -1):
        h[k] = temp % n
        temp //= n
        
    c_new = h[R-1]
    
    for i in range(R - 1):
        c_prev = h[i]
        dist = (R - 1) - i
        if c_prev == c_new:
            return 0
        d = c_prev - c_new
        if d == dist or d == -dist:
            return 0
            
    suffix_idx = idx // n 
    total_paths = 0
    
    for x in range(n):
        if x == c_new: 
            continue
        
        d_far = x - c_new
        if d_far == R or d_far == -R: 
            continue
        
        parent_idx = x * high_multiplier + suffix_idx
        total_paths += prev_counts[parent_idx]
        
    return total_paths

@njit(parallel=True, fastmath=True, cache=True)
def run_dp(n, limit):
    R = limit
    state_size = n ** R
    
    counts = np.zeros(state_size, dtype=np.int64)
    
    for idx in prange(state_size):
        counts[idx] = get_initial_count(idx, n, R)
            
    prev_counts = counts
    high_multiplier = n ** (R - 1)
    
    for step in range(R, n):
        curr_counts = np.zeros(state_size, dtype=np.int64)
        
        for idx in prange(state_size):
            curr_counts[idx] = compute_transition_kernel(idx, n, R, prev_counts, high_multiplier)
            
        prev_counts = curr_counts

    return np.sum(prev_counts)

def solve_problem_534(n_val):
    total_S = 0
    dp_limit_cutoff = 7
    
    for w in tqdm(range(n_val)):
        limit = n_val - 1 - w
        term = 0
        
        if limit == 0:
            term = n_val ** n_val
        elif limit <= dp_limit_cutoff:
            term = run_dp(n_val, limit)
        else:
            term = run_backtracking(n_val, limit)
            
        total_S += term
        
    return total_S

def main():
    result = solve_problem_534(14)
    print(result)

if __name__ == "__main__":
    main()