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
    """
    Purpose
    -------
    Computes the sum of M(C, 30) for 3 <= C <= 40, where M(C, R) is the minimum
    number of security cards required to travel through R rooms while carrying
    at most C cards at any time, for Project Euler problem 327.

    Method / Math Rationale
    -----------------------
    The algorithm computes M(C, R) iteratively from the last room backward.
    Initialize need = 1 (cards required upon entering the last room to avoid
    being trapped). For each preceding room, if need < C, set new_need = need + 1
    (plus one for entering the next room). If need >= C, compute the number of
    round-trip transports required to deposit the excess cards: each trip
    deposits (C - 2) cards net (1 for entry, 1 for return) at cost C cards per
    trip. The number of trips 'moves' is calculated as floor((need - C) / T) and
    adjusted if necessary to ensure remaining need < C after transports, where
    T = C - 2. Then new_need = remaining_need + consumed + 1. This ensures the
    minimum cards accounting for all door crossings and deposits.

    Complexity
    ----------
    O(R * (max_C - min_C)), as each of the (max_C - min_C + 1) values of C
    requires O(R) room iterations, each O(1) time due to closed-form moves
    calculation.

    References
    ----------
    https://projecteuler.net/problem=327
    """

    rooms = 30
    min_c = 3
    max_c = 40
    result = 0
    for c in range(min_c, max_c + 1):
        result += search(c, rooms)
    print(result)


if __name__ == "__main__":
    main()