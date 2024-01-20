# Problem: https://projecteuler.net/problem=29

def main():
    distinct_terms = set()

    for a in range(2, 101):
        for b in range(2, 101):
            distinct_terms.add(a**b)

    answer = len(distinct_terms)
    print(answer)

if __name__ == "__main__":
    main()
