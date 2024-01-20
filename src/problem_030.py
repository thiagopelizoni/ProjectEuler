# Problem: https://projecteuler.net/problem=30

def sum_of_powers_of_digits(n, power):
    return sum(int(digit)**power for digit in str(n))

def main():
    power  = 5
    limit  = 9**power * 6
    answer = 0

    for i in range(2, limit):
        if i == sum_of_powers_of_digits(i, power):
            answer += i

    print(answer)

if __name__ == "__main__":
    main()
