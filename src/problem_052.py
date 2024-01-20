# Problem: https://projecteuler.net/problem=52
def answer():
    x = 1
    while True:
        if all(sorted(str(x)) == sorted(str(x * i)) for i in range(2, 7)):
            return x
        x += 1

print(answer())
