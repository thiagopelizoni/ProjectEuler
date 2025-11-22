# Problem: https://projecteuler.net/problem=436
import sympy as sp

def main():
    e = sp.E
    y = sp.symbols('y')
    F = e * y + sp.exp(1 - y) - e
    Q = e * (e - 1) - sp.exp(1 - y) * (e - 1 + y)
    integrand = Q * F
    ans = sp.integrate(integrand, (y, 0, 1))
    prob = ans.evalf(12)
    print(f"{prob:.10f}")

if __name__ == "__main__":
    main()