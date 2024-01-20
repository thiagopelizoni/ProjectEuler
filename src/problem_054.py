# Problem: https://projecteuler.net/problem=54
import requests

def fetch_poker_hands():
    url = 'https://projecteuler.net/project/resources/p054_poker.txt'
    response = requests.get(url)
    return response.text.splitlines()

def evaluate_hand_rank(hand):
    card_values = '23456789TJQKA'
    value_dict = {value: index for index, value in enumerate(card_values)}
    suits = [card[1] for card in hand]
    values = sorted([value_dict[card[0]] for card in hand], reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = all(values[i] - values[i + 1] == 1 for i in range(4))

    value_counts = {value: values.count(value) for value in values}
    value_counts = sorted(value_counts.items(), key=lambda x: (-x[1], -x[0]))

    if is_straight and is_flush:
        return (8, values)
    elif value_counts[0][1] == 4:
        return (7, value_counts[0][0], value_counts[1][0])
    elif value_counts[0][1] == 3 and value_counts[1][1] == 2:
        return (6, value_counts[0][0], value_counts[1][0])
    elif is_flush:
        return (5, values)
    elif is_straight:
        return (4, values)
    elif value_counts[0][1] == 3:
        return (3, value_counts[0][0], values)
    elif value_counts[0][1] == 2 and value_counts[1][1] == 2:
        return (2, value_counts[0][0], value_counts[1][0], values)
    elif value_counts[0][1] == 2:
        return (1, value_counts[0][0], values)
    else:
        return (0, values)

def compare_poker_hands(hand1, hand2):
    return evaluate_hand_rank(hand1) > evaluate_hand_rank(hand2)

def count_winning_hands(hands):
    count = 0
    for hand in hands:
        cards = hand.split()
        if compare_poker_hands(cards[:5], cards[5:]):
            count += 1
    return count

poker_hands = fetch_poker_hands()
print(count_winning_hands(poker_hands))
