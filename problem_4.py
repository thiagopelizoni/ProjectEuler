def is_palindrome(n):
    return str(n) == str(n)[::-1]

def largest_palindrome_product():
    largest_palindrome = 0
    for i in range(100, 1000):
        for j in range(100, 1000):
            product = i * j
            if is_palindrome(product) and product > largest_palindrome:
                largest_palindrome = product
    return largest_palindrome

if __name__ == "__main__":
    print(largest_palindrome_product())
