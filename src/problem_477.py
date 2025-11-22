# Problem: https://projecteuler.net/problem=477
from tqdm import tqdm

def main():
    MOD = 1000000007
    N = 10**8
    s = [0] * N
    current = 0
    total_sum = 0
    for i in tqdm(range(N)):
        s[i] = current
        total_sum += current
        current = (current * current + 45) % MOD

    sc = []
    for v in s:
        sc.append(v)
        while len(sc) >= 3 and sc[-3] <= sc[-2] and sc[-2] >= sc[-1]:
            new_v = sc[-3] - sc[-2] + sc[-1]
            sc.pop()
            sc.pop()
            sc[-1] = new_v

    sorted_sc = sorted(sc, reverse=True)
    val = 0
    sign = 1
    for x in sorted_sc:
        val += sign * x
        sign = -sign

    result = (total_sum + val) // 2
    print(result)

if __name__ == "__main__":
    main()