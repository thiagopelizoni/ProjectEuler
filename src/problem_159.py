# Problem: https://projecteuler.net/problem=159
def digital_root(value):
    remainder = value % 9
    return 9 if remainder == 0 else remainder

def solve():
    upper_limit = 10 ** 6
    max_root_values = [0] * upper_limit

    for number in range(2, upper_limit):
        max_root_values[number] = digital_root(number)

    half_limit = upper_limit // 2 + 1

    for divisor in range(2, half_limit):
        multiple = divisor * 2
        while multiple < upper_limit:
            candidate_value = max_root_values[divisor] + max_root_values[multiple // divisor]
            if candidate_value > max_root_values[multiple]:
                max_root_values[multiple] = candidate_value
            multiple += divisor

    total_sum = sum(max_root_values[2:])
    print(total_sum)

if __name__ == "__main__":
    solve()
