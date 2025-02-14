#!/usr/bin/python3
""""""

# global failed_num_index


def safe_report_two(report: list):
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

    
    failed_num_index = None
    total_fails = 0

    def check_sequence(seq: list):
        """Checks if a sequence follows the safety rules."""
        nonlocal failed_num_index, total_fails  # Modify outer function variabless
        if total_fails == 2:
            return False
        increase = None
        for i in range(1, len(seq)):
            diff = seq[i] - seq[i - 1]
            
            if diff == 0 or abs(diff) > 3:
                failed_num_index = i
                print(f'in Fail 1 - failed num index {failed_num_index} : i = {i}')
                total_fails += 1
                return False
            
            if increase is None:
                increase = diff > 0  # Determine direction on first valid comparison
            elif (increase and diff < 0) or (not increase and diff > 0) or failed_num_index == 2:
                failed_num_index = i
                print(f'in Fail 1 - failed num index {failed_num_index} : i = {i}')
                total_fails += 1
                return False  # Direction changed, invalid sequence
        
        return True
    
    # First, check if the report is already valid
    if check_sequence(report):
        return True
    
    # If not, try removing one element at a time and rechecking

    print(f'failed num index {failed_num_index}')
    modified_report = report[:failed_num_index] + report[failed_num_index + 1:]
    print(f"Modified report: {modified_report}")
    if check_sequence(modified_report):
        if total_fails == 2:
            return False
        return True
    
    return False  # If no single removal fixes it, it's unsafe


#  ***********************************************************************************************************

# def safe_report_two(report: list):
#     """Determines if a report is safe or not
#     RULES:
#     The levels are either all increasing or all decreasing.
#     Any two adjacent levels differ by at least one and at most three.

#     7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
#     1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
#     9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
#     1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
#     8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
#     1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3."""

#     if not report:
#         return False
    
#     increase = None

#     # part two of the problem is to introduce a 'Problem Dampener'. This means
#     # that we can remove one, and only one, level (number of the list) from the list to make it safe.
#     # exampe:
#     # 7 6 4 2 1: Safe without removing any level.
#     # 1 2 7 8 9: Unsafe regardless of which level is removed.
#     # 9 7 6 2 1: Unsafe regardless of which level is removed.
#     # 1 3 2 4 5: Safe by removing the second level, 3.
#     # 8 6 4 4 1: Safe by removing the third level, 4.
#     # 1 3 6 7 9: Safe without removing any level.
#     problem_dampener = 0
#     safety_status = False

#     # range(1, len(report))
#     # This starts from index 1 (second element) and goes up to the last index.
#     # We don't start at 0 because we need to compare each element with the one before it.
#     for i in range(1, len(report)):
#         print(f"i = {i}\n")

#         # only one level can be removed from the list to make it safe
#         if problem_dampener == 2:
#             return False
                  
#         # first check if the difference is 1, 2, or 3
#         # report[i-1] is the previous element of the list
#         diff = report[i] - report[i - 1]

#         if diff == 0 or abs(diff) > 3:  # Difference must be 1, 2, or 3
#             # return safety_status
#             problem_dampener += 1
#             break

#         if increase is None:  # First comparison determines direction
#             increase = diff > 0 # True if increasing, False if decreasing
#         elif increase and diff < 0:  # If was increasing but now decreasing, fail
#             i += 1
#             problem_dampener += 1
#             # safety_status = False
#             break
#         elif not increase and diff > 0:  # If was decreasing but now increasing, fail
#             # safety_status = False
#             i += 1
#             problem_dampener += 1
#             break
            
        
#         # if safety_status is False:
#         #     # If we have already successfully removed a number from the list, we can't remove another one
#         #     # check the problem_dampener variable has been set to True and fail the test
#         #     if problem_dampener is True:
#         #         return False
#         #     # remove this number from the list and check if the list is safe
#         #     i += 1
#         #     problem_dampener = True
        
    
#     return safety_status