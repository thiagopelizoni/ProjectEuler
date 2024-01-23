# Problem: https://projecteuler.net/problem=100
# Define a function to find the number of blue discs for which the probability of drawing two blue discs
# is exactly 50% given the total number of discs.

def find_number_of_blue_discs(limit):
    # Start with the example provided in the problem statement
    b, n = 15, 21  # initial blue and total discs
    
    # Use the proportion of 50% chance for two blue discs to find the next arrangement
    while n < limit:
        btemp = 3 * b + 2 * n - 2
        ntemp = 4 * b + 3 * n - 3
        
        b, n = btemp, ntemp

    return b, n

# Find the first arrangement over 10^12 = 1_000_000_000_000 discs
limit = 10**12

blue_discs, total_discs = find_number_of_blue_discs(limit)
print(blue_discs)

