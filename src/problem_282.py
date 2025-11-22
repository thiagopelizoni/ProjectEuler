# Problem: https://projecteuler.net/problem=282
def get_lambda(m: int) -> int:
    if m == 1:
        return 1
    e = 0
    temp = m
    while temp % 7 == 0:
        temp //= 7
        e += 1
    if temp == 1:
        return 6 * (7 ** (e - 1)) if e >= 1 else 0
    elif temp == 6 or temp == 3:
        if e == 0:
            return 2
        else:
            return 6 * (7 ** (e - 1))
    elif temp == 2:
        return 1
    raise ValueError(f"Unexpected m: {m}")

def hyper_mod(arrows: int, height: int, mod_: int) -> int:
    if mod_ == 1:
        return 0
    if height == 0:
        return 1
    if height == 1:
        return 2 % mod_
    from math import gcd
    g = gcd(2, mod_)

    if arrows == 1:
        if g == 1:
            return pow(2, height, mod_)
        else:
            a = 0
            m = mod_
            while m % 2 == 0:
                m //= 2
                a += 1
            m_odd = m
            res_odd = pow(2, height, m_odd)
            mod2 = 2 ** a
            if height < a:
                res2 = pow(2, height, mod2)
            else:
                res2 = 0
            inv2 = pow(mod2, -1, m_odd)
            inv_odd = pow(m_odd, -1, mod2)
            x = (res2 * m_odd * inv_odd + res_odd * mod2 * inv2) % mod_
            return x

    if g == 1:
        lam = get_lambda(mod_)
        exponent = hyper_mod(arrows, height - 1, lam)
        return hyper_mod(arrows - 1, exponent, mod_)
    else:
        a = 0
        m = mod_
        while m % 2 == 0:
            m //= 2
            a += 1
        m_odd = m
        res_odd = hyper_mod(arrows, height, m_odd)
        mod2 = 2 ** a
        res2 = 0  # assuming large enough for arrows > 1
        inv2 = pow(mod2, -1, m_odd)
        inv_odd = pow(m_odd, -1, mod2)
        x = (res2 * m_odd * inv_odd + res_odd * mod2 * inv2) % mod_
        return x

def main():
    mod = 14 ** 8
    m1 = 2 ** 8
    m2 = 7 ** 8
    sum1 = 0
    sum2 = 0
    for mod_ in [m1, m2]:
        local_sum = 0
        for n in range(7):
            if n == 0:
                a = 1
            elif n == 1:
                a = 3
            elif n == 2:
                a = 7
            elif n == 3:
                a = 61
            else:
                if mod_ == m1:
                    a = 253
                else:
                    arrows = n - 2
                    height = n + 3
                    hyp = hyper_mod(arrows, height, mod_)
                    a = (hyp - 3) % mod_
            local_sum = (local_sum + a) % mod_
        if mod_ == m1:
            sum1 = local_sum
        else:
            sum2 = local_sum
    inv2 = pow(m2, -1, m1)
    inv1 = pow(m1, -1, m2)
    result = (sum1 * m2 * inv2 + sum2 * m1 * inv1) % mod
    print(result)

if __name__ == "__main__":
    main()