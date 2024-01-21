# Problem: https://projecteuler.net/problem=62
def main():
    count = 0
      # The base ranges from 1 to 9
    for n in range(1, 10):
          # The power can start from 1 and go up to 21 (since 9**22 has more than 22 digits)
        for power in range(1, 22):
            result = n ** power
            if len(str(result)) == power:
                count += 1
    return count

if __name__ == "__main__":
    print(main())
