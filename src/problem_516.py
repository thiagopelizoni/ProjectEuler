# Problem: https://projecteuler.net/problem=516
from gmpy2 import is_prime
import bisect
from tqdm import tqdm
 
def main():
    limit = 10**12

    hamming = []
    special_primes = []

    two = 1
    while two <= limit:
        three = 1
        while two * three <= limit:
            five = 1
            while two * three * five <= limit:
                current = two * three * five
                hamming.append(current)
                if current > 5 and is_prime(current + 1):
                    special_primes.append(current + 1)
                five *= 5
            three *= 3
        two *= 2
    hamming.sort()
    special_primes.sort()

    prefix = [0]
    for h in hamming:
        prefix.append(prefix[-1] + h)

    stack = [(1, 1)]
    total_sum = 0

    with tqdm(desc="Processing candidates", unit=" cand") as pbar:
        while stack:
            m, max_p = stack.pop()
            pbar.update(1)
            if m > limit:
                continue
            M = limit // m
            idx = bisect.bisect_right(hamming, M)
            sum_h = prefix[idx]
            total_sum += m * sum_h
            start_idx = bisect.bisect_right(special_primes, max_p)
            for i in range(start_idx, len(special_primes)):
                p = special_primes[i]
                next_m = m * p
                if next_m > limit:
                    break
                stack.append((next_m, p))
    
    result = total_sum % (1 << 32)

    print(result)

if __name__ == "__main__":
    main()