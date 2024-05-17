# Problem: https://projecteuler.net/problem=84
import numpy as np
import random

def main():
    dice_size = 4
    show_fields = 3

    rolls = 1000000  # Number of simulated moves
    num_fields = 40

    go = 0
    jail = 10
    go_to_jail = 30
    community = [2, 17, 33]
    chance = [7, 22, 36]
    next_railway = [15, 25, 5]  # index x corresponds to Chance[x]
    next_utility = [12, 28, 12]  # index x corresponds to Chance[x]

    chance_cards = list(range(16))
    community_cards = list(range(16))
    random.shuffle(chance_cards)
    random.shuffle(community_cards)

    current = go
    doubles = 0
    count = np.zeros(num_fields, dtype=np.int64)

    for _ in range(rolls):
        dice1 = random.randint(1, dice_size)
        dice2 = random.randint(1, dice_size)
        next_pos = (current + dice1 + dice2) % num_fields

        if dice1 == dice2:
            doubles += 1
        else:
            doubles = 0

        if doubles == 3:
            next_pos = jail
            doubles = 0

        if next_pos in chance:
            id = chance.index(next_pos)
            card = chance_cards.pop(0)
            chance_cards.append(card)

            if card == 0:
                next_pos = go
            elif card == 1:
                next_pos = jail
            elif card == 2:
                next_pos = 11  # C1
            elif card == 3:
                next_pos = 24  # E3
            elif card == 4:
                next_pos = 39  # H2
            elif card == 5:
                next_pos = 5   # R1
            elif card == 6:
                next_pos = (next_pos - 3) % num_fields
            elif card in (7, 8):
                next_pos = next_railway[id]
            elif card == 9:
                next_pos = next_utility[id]

        if next_pos in community:
            card = community_cards.pop(0)
            community_cards.append(card)

            if card == 0:
                next_pos = go
            elif card == 1:
                next_pos = jail

        if next_pos == go_to_jail:
            next_pos = jail

        count[next_pos] += 1
        current = next_pos

    total = np.sum(count)
    probabilities = count / total * 100

    sorted_indices = np.argsort(probabilities)[::-1]

    result = "".join(f"{idx:02}" for idx in sorted_indices[:show_fields])
    print(result)

if __name__ == "__main__":
    main()
