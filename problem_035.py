# Problem: https://projecteuler.net/problem=35
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def circular_primes(limit):
    count = 0
    for num in range(2, limit):
        str_num = str(num)
        if all(is_prime(int(str_num[i:] + str_num[:i])) for i in range(len(str_num))):
            count += 1
    return count

limit = 1000000
answer = circular_primes(limit)
print(answer)
