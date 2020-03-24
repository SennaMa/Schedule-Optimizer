################################################################################

""" Learnings:

DICTIONARY TERMS:

k = {"a":1, "b":2}
k.keys() = ['a','b']
k.values() = [1,2]
k.items() = [('a',1),('b',2)]

CONTENTS:

In intervals list, your initial key = number and pair = dictionary
The nested dictionary has key = number and pair = list


ITERATING:

for key in k.keys():
    # first it's "a" then "b"

for value in k.values():
    # first its 1 then 2

for key, value in k.items():
    # key and value are "a"
    # then "b" 2

SHORTCUTS:
Press (shift + tab) to redent multiple lines of code
Press tab to indent multiple lines of code

"""

################################################################################

# running packages
import pandas as pd
from collections import OrderedDict


"""
for this example, we only use intervals 8-9, 9-10, 10-11, 11-12 and morning counts as 8-9, aft counts as 9-11, eve counts as 11-12
"""

vacations = {
    "bob": [10, 14],
    "senna": [11, 13],
    "abed": [12, 13]
}


required = {
    "bob": 6,
    "senna": 7,
    "abed": 6
}

preferences = {
    "bob": {
        10: ["morn", "aft"],
        11: [],
        12: ["eve"],
        13: [],
        14: []
    },
    "senna": {
        10: [],
        11: ["eve"],
        12: [],
        13: [],
        14: ["morn"]
    },
    "abed": {
        10: ["morn"],
        11: ["morn"],
        12: ["eve"],
        13: [],
        14: ["morn"]
    }
}


headcounts = {
    10: {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    11: {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    12: {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    13: {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    14: {
        8: 1,
        9: 1,
        10: 1,
        11: 0
    }
}

intervals = {
    10: {
        8: ["test_dup","test_for_morning_shift", "senna","test_dup"],
        9: ["random"],
        10: ["random"],
        11: ["random","test_for_evening_shift"]
    },
    11: {
        8: ["bob","test_for_evening_shift"],
        9: ["bob"],
        10: ["random"],
        11: ["random"]
    },
    12: {
        8: ["senna"],
        9: ["bob"],
        10: ["random"],
        11: ["random"]
    },
    13: {
        8: ["random"],
        9: ["bob"],
        10: ["random"],
        11: ["random"]
    },
    14: {
        8: ["end_morning_shift_test", "senna"],
        9: ["abed"],
        10: ["random"],
        11: ["end_evening_shift_test"]
    }
}


################################################################################
# defining variables
""" we assume that only one HC per time slot for now """

# creating a tuple for hours that count as evening shifts. we use a tuple because evening shifts do not change unless we declare a change
evening_shift = (11,12) # not sure why but I'm unable to pull multiple hours
evening_shift_folks = {}
morning_shift_folks = {}


################################################################################
# sum of hours available per person
def sumOfHoursAvailable():
    sum = 0
    for person, hours in required.items():
        sum += hours
    return sum


# sum of hours required in the week to be filled
def numberOfHoursNeeded():
    sum_needed = 0
    for date, hours_of_day in headcounts.items():
        # at this point, we have access to the breakdowns per day
        hours_in_this_day = 0 # this is the sum of usable hours in the day
        for hour, hours_required in hours_of_day.items():
            hours_in_this_day += hours_required
        sum_needed += hours_in_this_day
    return sum_needed


# makes sure that the condition inside the assert is True, if not exit script
assert(numberOfHoursNeeded() <= sumOfHoursAvailable())

# [ ] looks at the intervals variable and returns true if schedule meets requirement
# [x] cant double book a call agent in the same time shift
# [x] required hours check = all required hours are met (equal or greater than)
# [x] if scheduled after vacation or evening shift, don't schedule morning shift
# [x] vacation check = not scheduled on vacation
# [x] head count is filled, no more no less

def meets_requirements():

    ##########################################################################
    # vacation check
    for name, days_off in vacations.items():
        for date in days_off:

            for scheduled_people_in_a_certain_hour in intervals[date].values():
                if name in scheduled_people_in_a_certain_hour:
                    print("{} got scheduled on {}, but it's a vacation".format(name, date))
                    return False

    ##########################################################################
    # required hours check
    for name, number_of_hours_required in required.items():
        number_of_times_name_pops_up = 0
        for date, hours in intervals.items():
            for hour, scheduled_people in hours.items():

                if name in scheduled_people:
                    number_of_times_name_pops_up += 1
        print(number_of_times_name_pops_up) # printing 7 right now for bob, 3 for senna, and N/A for abed (?)
        # at this point, number of times name pops up is the right amount
        if number_of_times_name_pops_up < number_of_hours_required:
            print("{} popped up {} time(s) but requires {}".format(name,number_of_times_name_pops_up, number_of_hours_required))
            return False


    ##########################################################################
    # if scheduled after vacation don't schedule morning shift

    for name, days_off in vacations.items():
        for date in days_off:
            vacay_consideration = date + 1  # finding the vacation date plus one to prevent people to be scheduled on this date
            for scheduled_people_in_a_certain_hour in intervals[vacay_consideration].values():
                if name in scheduled_people_in_a_certain_hour:
                    print("{} got scheduled on {}, but they were on vacation yesterday".format(name, vacay_consideration))
                    return False

    return True



def head_count_requirements():

    ##########################################################################
    # head count is filled, no more no less
    # count number of people in each interval. if count =/= headcount then return an error

    for date, hours in headcounts.items():
        for hour, required_hours in hours.items():
            head_count_hours = 0
            head_count_hours += required_hours
            #print(head_count_hours)                # testing how many head_counts

    for date, hours in intervals.items():
        for hour, scheduled_people in hours.items():
            interval_count = 0
            interval_count += len(scheduled_people)
            #print(interval_count)                           # testing how many counts

    if interval_count!= head_count_hours:
        print("the number of people scheduled do not match the number of people required. there are {} people scheduled but we need {} during this time shift".format(interval_count,head_count_hours))
        return False

    return True


def vacay_evening_check():

    ##########################################################################
    # if scheduled for evening shift, don't schedule morning shift

    for date, hours in intervals.items():
        evening_shift_consideration = date + 1

        for hour, scheduled_people in hours.items():
            if hour >= 11:              # PLEASE SEE LINE 150. Should be if hour == evening_shift, but I can't get var to work
                evening_shift_folks[date] = scheduled_people

            if hour <= 8:
                morning_shift_folks[date] = scheduled_people

    for date, eve_scheduled_people in evening_shift_folks.items():
        if date < max(evening_shift_folks.keys()):

            # if any(evening_shift_folks[date] in morning_shift_folks[date + 1]):
            potential_booking_errors = [
                person for person in eve_scheduled_people if person in morning_shift_folks[date + 1]]
            if len(potential_booking_errors) > 0:           # if no errors then produce empty list == 0
                print("Can't book {list_of_ppl} for morning shift on {date}".format(
                    list_of_ppl=potential_booking_errors,
                    date=date))

    return True



def double_book_check():

    ##########################################################################
    # cannot double book a call agent in the same time shift


    for date, hours in intervals.items():
        for hour, scheduled_people in hours.items():
            new_list = []
            new_list = sorted(scheduled_people)     # creates a new list and sorts the values so we can find dups

            if (len(new_list) >= 2) and (len(new_list) != len(set(new_list))):
                 print("{} is a duplicate".format(new_list))

            else:
                continue


            # duplicate_check = [print("{} is a duplicate".format(new_list[x])) for person in new_list
            #                     if (len(new_list) >=2) and new_list[x] == new_list[x+1]]





    # looks at the intervals variable and returns true if schedule meets requirement



#print("sum of available hours: {}".format(sumOfHoursAvailable()))
#print("  total required hours: {}".format(numberOfHoursNeeded()))
#print("meets requirements? {}".format(meets_requirements()))
#print(head_count_requirements())
print(pd.DataFrame.from_dict(intervals))
#vacay_evening_check()
#double_book_check()





