# Problem: https://projecteuler.net/problem=109
def main():
    points = [i * j for i in range(1, 21) for j in range(1, 4)] + [25, 50]
    double_points = [i * 2 for i in range(1, 21)] + [25 * 2]

    ways = [[[None] * len(points) for j in range(101)] for i in range(3)]

    def calc_ways(throws, total, max_index):
        if ways[throws][total][max_index] is None:
            if throws == 0:
                result = 1 if total == 0 else 0
            else:
                result = 0
                if max_index > 0:
                    result += calc_ways(throws, total, max_index - 1)
                if points[max_index] <= total:
                    result += calc_ways(throws - 1, total - points[max_index], max_index)
            ways[throws][total][max_index] = result
        return ways[throws][total][max_index]

    checkouts = 0
    for remaining_points in range(1, 100):
        for throws in range(3):
            for p in double_points:
                if p <= remaining_points:
                    checkouts += calc_ways(throws, remaining_points - p, len(points) - 1)
    return str(checkouts)

if __name__ == "__main__":
    print(main())