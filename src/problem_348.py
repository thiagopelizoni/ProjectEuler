# Problem: https://projecteuler.net/problem=348
import heapq

def is_palindrome(n):
    return str(n) == str(n)[::-1]

def main():
    heap = []
    visited = set()
    initial_s = 2
    initial_c = 2
    initial_v = initial_s ** 2 + initial_c ** 3
    heapq.heappush(heap, (initial_v, initial_s, initial_c))
    visited.add((initial_s, initial_c))
    num_found = 0
    total_sum = 0
    while heap:
        current_v = heap[0][0]
        ways = []
        while heap and heap[0][0] == current_v:
            v, s, c = heapq.heappop(heap)
            ways.append((s, c))
            for ds, dc in [(1, 0), (0, 1)]:
                next_s = s + ds
                next_c = c + dc
                next_key = (next_s, next_c)
                if next_key not in visited:
                    visited.add(next_key)
                    next_v = next_s ** 2 + next_c ** 3
                    heapq.heappush(heap, (next_v, next_s, next_c))
        if len(ways) == 4:
            if is_palindrome(current_v):
                total_sum += current_v
                num_found += 1
                if num_found == 5:
                    print(total_sum)
                    return

if __name__ == "__main__":
    main()