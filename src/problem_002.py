# Problem: https://projecteuler.net/problem=2
from tqdm import tqdm

LIMIT = 4000000

def sum_even_fibonacci(limit: int) -> int:
    total_sum = 0
    a, b = 2, 8
    
    with tqdm() as pbar:
        while a <= limit:
            total_sum += a
            a, b = b, 4 * b + a
            pbar.update(1)
        
    return total_sum

if __name__ == "__main__":
    answer = sum_even_fibonacci(LIMIT)
    print(answer)
