# Problem: https://projecteuler.net/problem=308
import numba
from numba import njit, int64

@njit(int64(int64))
def compute_steps(num_primes):
    S_ = int64(0)
    S11 = int64(1)
    S13 = int64(2)
    S17 = int64(3)
    S19 = int64(4)
    S23 = int64(5)
    S29 = int64(6)
    state = S_
    two = int64(1)
    three = int64(0)
    five = int64(0)
    seven = int64(0)
    steps = int64(0)
    num_found = int64(0)
    while True:
        if state == S_:
            if three == 0 and five == 0 and seven == 0 and steps > 0:
                num_found += 1
                if num_found == num_primes:
                    return steps
            if two > 0:
                steps += two
                three += two
                five += two
                two = 0
                continue
            if seven > 0:
                steps += seven
                seven = 0
                continue
            five += 1
            state = S11
            steps += 1
            continue
        elif state == S11:
            if three > 0:
                steps += 2 * three
                seven += three
                three = 0
                continue
            state = S13
            steps += 1
            continue
        elif state == S13:
            if seven > 0:
                if five > 0:
                    smallest = min(five, seven)
                    steps += 2 * smallest
                    two += smallest
                    three += smallest
                    five -= smallest
                    seven -= smallest
                    continue
                seven -= 1
                state = S17
                steps += 1
                continue
            state = S11
            steps += 1
            continue
        elif state == S17:
            if five > 0:
                five -= 1
                two += 1
                three += 1
                state = S13
                steps += 1
                continue
            if three > 0:
                three -= 1
                state = S19
                steps += 1
                continue
            state = S_
            steps += 1
            continue
        elif state == S19:
            if two > 0:
                steps += 2 * two
                five += two
                two = 0
                continue
            seven += 1
            state = S11
            steps += 1
            continue
        elif state == S23:
            five += 1
            state = S19
            steps += 1
            continue
        elif state == S29:
            seven += 1
            state = S11
            steps += 1
            continue

def main():
    print(compute_steps(10001))

if __name__ == "__main__":
    main()