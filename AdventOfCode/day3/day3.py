#!/usr/bin/python3

import re
"""Using the Regular Expression library to complete day 3, re module allows to match the pattern we're looking for"""


def get_total(matches: list):
    """
    """
    total = 0
    for match in matches:
        nums = match[4:-1] 
        a, b = nums.split(",")
        total += int(a) * int(b)
    return total


def get_matches(filename: str):
    """
    """
    regex_pattern = r"mul\(\d{1,3},\d{1,3}\)"
    with open(filename, 'r', encoding='utf-8') as f:
        
        matches = re.findall(regex_pattern, f.read())
    return matches


def main():
    mul_matches = get_matches("./puzzleinput.txt")
    total = get_total(mul_matches)
    print(total)
    


if __name__ == '__main__':
    main()