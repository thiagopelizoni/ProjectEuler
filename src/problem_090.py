# Problem: https://projecteuler.net/problem=90
from itertools import combinations

square_numbers = ['01', '04', '09', '16', '25', '36', '49', '64', '81']

def can_display(c1, c2):
    for square in square_numbers:
        if not ((square[0] in c1 and square[1] in c2) or (square[0] in c2 and square[1] in c1)):
            if '6' in square or '9' in square:
                square = square.replace('6', '9') if '6' in square else square.replace('9', '6')
                if not ((square[0] in c1 and square[1] in c2) or (square[0] in c2 and square[1] in c1)):
                    return False
            else:
                return False
    return True

combinations_cube = list(combinations('0123456789', 6))

distinct_arrangements = 0
for i in range(len(combinations_cube)):
    for j in range(i, len(combinations_cube)):
        if can_display(combinations_cube[i], combinations_cube[j]):
            distinct_arrangements += 1

print(distinct_arrangements)
