def find_min_n(target):
    search_limit = 200000

    while True:
        layer_counts = [0] * (search_limit + 1)
        max_a = int((search_limit / 6) ** 0.5)

        for length_a in range(1, max_a + 1):
            length_b = length_a

            while True:
                if 4 * length_a * length_b + 2 * length_b * length_b > search_limit:
                    break

                length_c = length_b

                while True:
                    surface_area = 2 * (length_a * length_b + length_b * length_c + length_c * length_a)

                    if surface_area > search_limit:
                        break

                    sum_lengths = length_a + length_b + length_c
                    layer = 1

                    while True:
                        total_cubes = (
                            surface_area
                            + 4 * (layer - 1) * sum_lengths
                            + 4 * (layer - 1) * (layer - 2)
                        )

                        if total_cubes > search_limit:
                            break

                        layer_counts[total_cubes] += 1
                        layer += 1

                    length_c += 1

                length_b += 1

        for cubes, count in enumerate(layer_counts):
            if count == target:
                return cubes

        search_limit *= 2


def main():
    result = find_min_n(1000)
    print(result)


if __name__ == "__main__":
    main()
