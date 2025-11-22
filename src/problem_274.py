# Problem: https://projecteuler.net/problem=274
from sympy.ntheory import primerange
from tqdm import tqdm

def main():
    N: int = 10**7
    total: int = 0
    for p in tqdm(primerange(3, N)):
        if p == 5:
            continue
        m: int = pow(10, -1, p)
        total += m
    print(total)

if __name__ == "__main__":
    main()