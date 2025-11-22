# Problem: https://projecteuler.net/problem=301
from tqdm import tqdm

def main():
    a = 1
    b = 1
    for _ in tqdm(range(3, 33)):
        a, b = b, a + b
    print(b)

if __name__ == "__main__":
    main()