# Problem: https://projecteuler.net/problem=341
from tqdm import tqdm
from math import ceil

def main():
    limit = 1000000
    cubic_limit = limit ** 3
    golomb = [0, 1]
    sums = [0, 1]
    products = [0, 1]
    i = 1
    with tqdm(desc="Building sequence") as pbar:
        while products[-1] < cubic_limit:
            i += 1
            current = 1 + golomb[i - golomb[golomb[i - 1]]]
            golomb.append(current)
            sums.append(sums[-1] + current)
            products.append(products[-1] + current * i)
            pbar.update(1)
    total = 0
    index = 1
    for n in range(1, limit):
        p = n * n * n
        while products[index] < p:
            index += 1
        from_p = products[index - 1]
        to_p = products[index]
        ratio = (p - from_p) / (to_p - from_p)
        low = sums[index - 1]
        high = sums[index]
        offset = ceil((high - low) * ratio)
        g = low + offset
        total += g
    print(total)

if __name__ == "__main__":
    main()