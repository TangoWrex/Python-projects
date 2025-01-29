#!/usr/bin/env python3


def to_jaden_case(string):
    capitalString = ""
    for x, y in enumerate(string):
        if x == 0 or string[x - 1] == ' ':
            capitalString += y.upper()
        else:
            capitalString += y.lower()

    return(capitalString)


# convert numbers to string
def number_to_string(num):
    return str(num)


# Write a function, persistence, that takes in a positive parameter num and returns its
# multiplicative persistence, which is the number of times you must multiply the digits 
# in num until you reach a single digit.
def persistence(n):
    count = 0
    while n >= 10:
        numList = []
        for x in str(n):
            numList.append(int(x))
        n = 1
        for x in numList:
            n *= x
        count += 1
    print(count)
        


def pig_it(text):
    pig_string = ""
    for x in text.split():
        if x.isalpha():
            pig_string += x[1:] + x[0] + "ay "
        else:
            pig_string += x
    return pig_string.strip()





def main():
    # to_jaden_case("this is a test string")
    print(pig_it("Pig latin is cool"))

if __name__ == '__main__':
    main()