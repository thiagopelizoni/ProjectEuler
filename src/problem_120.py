# Problem: https://projecteuler.net/problem=120
import numpy as np

max_r = 0
for a in range(3, 1001):
    r_max = 2 * a * ((a - 1) // 2)
    max_r += r_max

print(max_r)
