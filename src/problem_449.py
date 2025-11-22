# Problem: https://projecteuler.net/problem=449
import math

def main():
    a = 3
    b = 1
    r = 1
    e = math.sqrt(1 - (b / a)**2)
    S = 2 * math.pi * a**2 + math.pi * (b**2 / e) * math.log((1 + e) / (1 - e))
    V_2 = S / 2
    int_val = a * (1 / (2 * e)) * (math.asin(e) + e * math.sqrt(1 - e**2))
    V_1 = 4 * int_val
    vol_choc = 2 * V_2 * r + math.pi * V_1 * r**2 + (4 / 3) * math.pi * r**3
    print(f"{vol_choc:.8f}")

if __name__ == "__main__":
    main()