# Problem: https://projecteuler.net/problem=37
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_truncatable_prime(n):
    if n < 10:
        return False

    str_n = str(n)
    for i in range(1, len(str_n)):
        if not is_prime(int(str_n[i:])) or not is_prime(int(str_n[:i])):
            return False
    return True

def truncatable_primes():
    count = 0
    total_sum = 0
    num = 11
    while count < 11:
        if is_prime(num) and is_truncatable_prime(num):
            total_sum += num
            count += 1
        num += 2
    return total_sum

answer = truncatable_primes()
print(answer)
