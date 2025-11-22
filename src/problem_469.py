# Problem: https://projecteuler.net/problem=469
from decimal import Decimal, getcontext

def main():
    getcontext().prec = 30
    exp_minus_2 = Decimal('-2').exp()
    e_n = (Decimal(1) + exp_minus_2) / Decimal(2)
    rounded = e_n.quantize(Decimal('1e-14'))
    print(f"{rounded:f}")

if __name__ == "__main__":
    main()