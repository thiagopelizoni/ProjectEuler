# Problem: https://projecteuler.net/problem=387
from sympy import isprime
from tqdm import tqdm

def main():
    limit = 10**14
    total = 0
    current_harshads = [(d, d) for d in range(1, 10)]
    for _ in tqdm(range(13)):
        new_harshads = []
        for num, s in current_harshads:
            quotient = num // s
            if isprime(quotient):
                for d in range(10):
                    candidate = num * 10 + d
                    if candidate < limit and isprime(candidate):
                        total += candidate
            for d in range(10):
                new_num = num * 10 + d
                new_s = s + d
                if new_s != 0 and new_num % new_s == 0:
                    new_harshads.append((new_num, new_s))
        current_harshads = new_harshads
    print(total)

if __name__ == "__main__":
    main()