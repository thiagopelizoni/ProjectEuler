# Problem: https://projecteuler.net/problem=300
import numpy as np
from numba import njit
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from tqdm import tqdm

@njit
def update_best(contacts, best):
    for mask in range(len(best)):
        score = 0
        for c in contacts:
            if (mask & c) == 0:
                score += 1
        if score > best[mask]:
            best[mask] = score

def search(curr_len, N, positions, occupied, last_x, last_y, visited):
    if curr_len == N:
        if positions[-1][1] < 0:
            return
        contacts = []
        for i in range(N):
            for j in range(i + 3, N):
                dx = abs(positions[i][0] - positions[j][0])
                dy = abs(positions[i][1] - positions[j][1])
                if dx + dy == 1:
                    pair = (1 << i) | (1 << j)
                    contacts.append(pair)
        contacts.sort()
        key = tuple(contacts)
        if key not in visited:
            visited.add(key)
        return
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    for d in range(4):
        nx = last_x + dx[d]
        ny = last_y + dy[d]
        if (nx, ny) not in occupied:
            positions.append((nx, ny))
            occupied.add((nx, ny))
            search(curr_len + 1, N, positions, occupied, nx, ny, visited)
            positions.pop()
            occupied.remove((nx, ny))

def compute_partial(chunk):
    N = 15
    partial = np.zeros(1 << N, dtype=np.int32)
    for tup in chunk:
        contacts = np.array(list(tup), dtype=np.uint64)
        update_best(contacts, partial)
    return partial

def main():
    N = 15
    visited = set()
    positions = [(0, 0), (1, 0)]
    occupied = set(positions)
    search(2, N, positions, occupied, 1, 0, visited)
    unique_contacts = list(visited)
    num_cpus = cpu_count()
    l = len(unique_contacts)
    chunk_size = (l // num_cpus) + 1
    chunks = [unique_contacts[i:i + chunk_size] for i in range(0, l, chunk_size)]
    with ProcessPoolExecutor() as executor:
        partials = list(executor.map(compute_partial, chunks))
    best = np.zeros(1 << N, dtype=np.int32)
    for p in partials:
        best = np.maximum(best, p)
    direct = np.zeros(1 << N, dtype=np.int32)
    for mask in tqdm(range(1 << N)):
        for k in range(N - 1):
            if (mask & (1 << k)) == 0 and (mask & (1 << (k + 1))) == 0:
                direct[mask] += 1
    best += direct
    total = np.sum(best)
    average = total / (1 << N)
    print(average)

if __name__ == "__main__":
    main()