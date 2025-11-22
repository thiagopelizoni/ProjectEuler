# Problem: https://projecteuler.net/problem=284
from tqdm import tqdm

class SteadyType:
    def __init__(self, start: int) -> None:
        self.a: int = start
        self.sum_digits: int = start
        self.n: int = 1
        self.k: int = (self.a ** 2 - self.a) // 14

    def step(self) -> int:
        c: int = (2 * self.a - 1) % 14
        inv_c: int = pow(c, -1, 14)
        k_mod: int = self.k % 14
        d: int = ((-k_mod) * inv_c) % 14
        pow_m1: int = pow(14, self.n)
        old_a: int = self.a
        self.a = self.a + d * pow_m1
        self.sum_digits += d
        self.n += 1
        self.k = (self.k + d * (2 * old_a - 1) + d ** 2 * pow_m1) // 14
        return d

def to_base14(num: int) -> str:
    if num == 0:
        return "0"
    s: str = ""
    while num > 0:
        r: int = num % 14
        if r < 10:
            s = str(r) + s
        else:
            s = chr(ord("a") + r - 10) + s
        num //= 14
    return s

def main() -> None:
    total: int = 1
    type7: SteadyType = SteadyType(7)
    type8: SteadyType = SteadyType(8)
    total += type7.sum_digits + type8.sum_digits
    max_n: int = 10000
    for _ in tqdm(range(2, max_n + 1)):
        d7: int = type7.step()
        d8: int = type8.step()
        if d7 > 0:
            total += type7.sum_digits
        if d8 > 0:
            total += type8.sum_digits
    print(to_base14(total))

if __name__ == "__main__":
    main()