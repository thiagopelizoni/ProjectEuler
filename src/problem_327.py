# Problem: https://projecteuler.net/problem=327
def search(cards: int, rooms: int) -> int:
    need = 1
    transport = cards - 2
    for _ in range(rooms):
        consumed = 0
        if need >= cards:
            moves = (need - cards) // transport
            if need - moves * transport >= cards:
                moves += 1
            need -= moves * transport
            consumed = moves * cards
        need = need + consumed + 1
    return need


def main():

    rooms = 30
    min_c = 3
    max_c = 40
    result = 0
    for c in range(min_c, max_c + 1):
        result += search(c, rooms)
    print(result)


if __name__ == "__main__":
    main()