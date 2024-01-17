# Problem: https://projecteuler.net/problem=26

def find_recurring_cycle_length(d):
    seen_remainders = {}
    value = 1
    position = 0

    while value not in seen_remainders:
        seen_remainders[value] = position
        value = (value * 10) % d
        position += 1

    if value == 0:
        return 0
    else:
        return position - seen_remainders[value]

def main():
    """ Find the number with the longest recurring cycle in its decimal fraction part """
    max_length = 0
    number = 0

    for i in range(1, 1000):
        current_length = find_recurring_cycle_length(i)
        if current_length > max_length:
            max_length = current_length
            number = i

    print(number)

if __name__ == "__main__":
    main()
