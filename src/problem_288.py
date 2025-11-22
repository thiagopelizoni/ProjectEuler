# Problem: https://projecteuler.net/problem=288
from tqdm import tqdm

def main():
    p = 61
    mod = 50515093
    q = 10000000
    S = 290797
    early_P = [0] * 11
    current_sum = 0
    last_P = []
    last_T = []
    for n in tqdm(range(q + 1)):
        T = S % p
        current_sum += T
        if n < 10:
            early_P[n + 1] = current_sum
        if n >= q - 9:
            last_P.append(current_sum)
        if n >= q - 8:
            last_T.append(T)
        S = (S * S) % mod
    S_total = 0
    pow_p = [p ** i for i in range(10)]
    for m in range(10):
        sum_m = last_P[m] - early_P[m + 1]
        S_total += sum_m * pow_p[m]
    for i in range(9):
        r = 8 - i
        temp = 0
        for m in range(r + 1):
            temp += last_T[i + m] * pow_p[m]
        S_total += temp
    mod_val = pow_p[9] * p
    result = S_total % mod_val
    print(result)

if __name__ == "__main__":
    main()