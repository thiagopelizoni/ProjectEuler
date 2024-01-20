# Problem: https://projecteuler.net/problem=17
def number_to_words(n):
    """
    Convert a number to its words representation.
    """
    if n == 0:
        return "zero"

    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    def convert_under_1000(number):
        if number < 20:
            return ones[number] if number < 10 else teens[number - 10]
        elif number < 100:
            return tens[number // 10] + (ones[number % 10] if number % 10 != 0 else "")
        else:
            return ones[number // 100] + "hundred" + (("and" + convert_under_1000(number % 100)) if number % 100 != 0 else "")

    words = ""
    if n == 1000:
        words = "onethousand"
    else:
        words = convert_under_1000(n)
    return words

def letter_count_1_to_1000():
    """
    Calculate the total number of letters used in writing all the numbers from 1 to 1000 (inclusive) in words.
    """
    return sum(len(number_to_words(i)) for i in range(1, 1001))

# Calculate the total letter count for numbers 1 to 1000
if __name__ == "__main__":
    answer = letter_count_1_to_1000()
    print(answer)
