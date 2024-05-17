# Problem: https://projecteuler.net/problem=121
from sympy import Rational

turns = 15
probabilities = [Rational(1, i + 2) for i in range(turns)]

win_prob = [0] * (turns + 1)
win_prob[0] = 1

for i in range(turns):
    for j in range(i, -1, -1):
        win_prob[j + 1] += win_prob[j] * probabilities[i]
        win_prob[j] *= 1 - probabilities[i]

win_total = sum(win_prob[turns // 2 + 1:])
prize = int(1 / win_total)
print(prize)