# Problem: https://projecteuler.net/problem=394
from decimal import Decimal, getcontext
import math

def main():
    getcontext().prec = 20
    x = Decimal(40)
    ln_x = Decimal(math.log(40))
    term1 = Decimal(7) / Decimal(9)
    term2 = (Decimal(2) / Decimal(3)) * ln_x
    term3 = (Decimal(2) / Decimal(9)) / (x ** 3)
    result = term1 + term2 + term3
    print(f"{result:.10f}")

if __name__ == "__main__":
    main()