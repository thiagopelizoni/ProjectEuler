# Problem: https://projecteuler.net/problem=19
from datetime import date

SATURDAY = 6

def main():
    sundays = 0
    for year in range(1901, 2001):
        for month in range(1, 13):
            if date(year, month, 1).weekday() == SATURDAY:
                sundays += 1
    print(sundays)

# Calculate the number of lattice paths for a 20x20 grid
if __name__ == "__main__":
    main()
