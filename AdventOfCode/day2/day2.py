#!/usr/bin/python3

from day2part2 import safe_report_two



def build_list(filename: str):
    """Reads a file and converts each line into a list of integers
    
    Change "9 12 14 16 17 18 15" to list [9, 12, 14, 16, 17, 18, 15]
    """
    with open(filename, 'r', encoding='utf-8') as f:
        num_list  = []
        for line in f:
            numbers = list(map(int, line.strip().split()))
            num_list.append(numbers)
        # print(f"Num List: {num_list}")
    return num_list


def is_line_safe(report: list):
    """Determines if a report is safe or not
    RULES:
    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.

    7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3."""

    if not report:
        return False
    
    increase = None

    # part two of the problem is to introduce a 'Problem Dampener'. This means
    # that we can remove one, and only one, level (number of the list) from the list to make it safe.
    # exampe:
    # 7 6 4 2 1: Safe without removing any level.
    # 1 2 7 8 9: Unsafe regardless of which level is removed.
    # 9 7 6 2 1: Unsafe regardless of which level is removed.
    # 1 3 2 4 5: Safe by removing the second level, 3.
    # 8 6 4 4 1: Safe by removing the third level, 4.
    # 1 3 6 7 9: Safe without removing any level.
    problem_dampener = 0
    # safety_status = False

    # range(1, len(report))
    # This starts from index 1 (second element) and goes up to the last index.
    # We don't start at 0 because we need to compare each element with the one before it.
    for i in range(1, len(report)):
                  
        # first check if the difference is 1, 2, or 3
        # report[i-1] is the previous element of the list
        diff = report[i] - report[i - 1]

        if diff == 0 or abs(diff) > 3:  # Difference must be 1, 2, or 3
            # return safety_status
            problem_dampener +=1
            return False

        if increase is None:  # First comparison determines direction
            increase = diff > 0
        elif increase and diff < 0:  # If was increasing but now decreasing, fail
            problem_dampener +=1
            print(problem_dampener)
            return False
        elif not increase and diff > 0:  # If was decreasing but now increasing, fail
            problem_dampener +=1
            print(problem_dampener)
            return False
        
        # if safety_status is False:
        #     # If we have already successfully removed a number from the list, we can't remove another one
        #     # check the problem_dampener variable has been set to True and fail the test
        #     if problem_dampener is True:
        #         return False
        #     # remove this number from the list and check if the list is safe
        #     i += 1
        #     problem_dampener = True
        
    
    return True

def calculate_safe_lines(num_list: list):
    """Counts the number of safe reports"""
    total_safe_lines = 0
    for reports in num_list:
        # if is_line_safe(reports):
        #     total_safe_lines += 1
        if safe_report_two(reports):
            total_safe_lines += 1

    return total_safe_lines


def main():
    num_list = build_list("./numbers.txt")
    safe_distance_count = calculate_safe_lines(num_list)
    print(safe_distance_count)


if __name__ == '__main__':
    main()