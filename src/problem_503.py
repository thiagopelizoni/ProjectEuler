# Problem: https://projecteuler.net/problem=503
from tqdm import tqdm

def main():
    n = 1000000
    f = [0.0] * (n + 1)
    f[n] = (n + 1.0) / 2
    up = n - 1
    for i in tqdm(range(n - 1, 0, -1)):
        f[i] = f[i + 1]
        prob = 1.0
        expe = 0.0
        for k in range(1, up + 1):
            expe += 1.0 / i * (n + 1) / (i + 1) * k
            if expe >= f[i]:
                break
            prob -= 1.0 / i
            if expe + prob * f[i + 1] < f[i]:
                f[i] = expe + prob * f[i + 1]
                up = k
    print(f"{f[1]:.10f}")

if __name__ == "__main__":
    main()