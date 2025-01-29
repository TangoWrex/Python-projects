#!/usr/bin/env python3
"""
Module that validates user input
Has various functions that check integer, float,
is number in range, is entry contained in

Functions continue to prompt until input
is valid
"""
from itertools import chain



def enter_valid_character(prompt, set_of_valid_chars: str, ignore_case=True):
 
    if ignore_case:
       
        set_of_valid_chars = set(chain([a_char.upper() for a_char in set_of_valid_chars],
                                       [a_char.lower() for a_char in set_of_valid_chars]))

    
    while (entered_char := input(prompt + "==> ")) not in set_of_valid_chars:
        print(f'{entered_char} not one of the valid characters {set_of_valid_chars}. Try again')

    return entered_char


def enter_number_in_range(prompt, low, high, entry_function):
    a_num = entry_function(prompt)
    while not low <= a_num <= high:
        print(f'{a_num} not between {low} and {high}. Try again')
        a_num = entry_function(prompt)

    return a_num


def enter_float_in_range(prompt, low, high):
    return enter_number_in_range(prompt, low, high, enter_a_float)


def enter_integer_in_range(prompt, low, high):
    return enter_number_in_range(prompt, low, high, enter_an_integer)


def enter_correct_type(prompt, type_function):
    input_valid = False
    while not input_valid:
        try:
            a_num = type_function(input(prompt + "==> "))
            return a_num
        except ValueError as ve:
            print(f"Value entered is not an {type_function.__name__}. Try again")


def enter_an_integer(prompt):
    return enter_correct_type(prompt, int)


def enter_a_float(prompt):
    return enter_correct_type(prompt, float)


def main():
    print(enter_integer_in_range("Enter integer between 1 and 5", 1, 5))
    print(enter_float_in_range("Enter float between 1.5 and 5.5", 1.5, 5.5))

    print(enter_an_integer('Enter integer'))
    print(enter_a_float('Enter float'))


if __name__ == "__main__":
    main()
