# Problem: https://projecteuler.net/problem=430
from decimal import Decimal, getcontext
from tqdm import tqdm

def main():
    getcontext().prec = 50
    N = 10000000000
    M = 4000
    DN = Decimal(N)
    DNN = DN ** 2
    s = Decimal(0)
    max_k = 20000000
    for i in tqdm(range(1, max_k + 1)):
        Di = Decimal(i)
        num = 4 * Di ** 2 - 4 * (DN + 1) * Di + DN ** 2 + Decimal(2)
        r = num / DNN
        term = r ** M
        if term < Decimal('1e-12'):
            break
        s += term

    total = 2 * s
    E = DN / 2 + Decimal('0.5') * total
    print('{:.2f}'.format(float(E)))

if __name__ == "__main__":
    main()