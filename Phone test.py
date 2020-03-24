################################################################################

""" Learnings:

DICTIONARY TERMS:

k = {"a":1, "b":2}
k.keys() = ['a','b']
k.values() = [1,2]
k.items() = [('a',1),('b',2)]



ITERATING:

for key in k.keys():
    # first it's "a" then "b"

for value in k.values():
    # first its 1 then 2

for key, value in k.items():
    # key and value are "a" 1
    # then "b" 2

SHORTCUTS:
Press (shift + tab) to reduce indent on multiple lines of code


"""





################################################################################


# New input data


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
        8: ["test_for_morning_shift, senna"],
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
        8: ["end_morning_shift_test, senna"],
        9: ["abed"],
        10: ["random"],
        11: ["end_evening_shift_test"]
    }
}





""" OLD INPUT DATA

vacations = {
    "bob": ["Mon 6", "Fri 10"],
    "senna": ["Tue 7", "Thu 9"],
    "abed": ['Wed 8', 'Thu 9']
}

required = {
    "bob": 6,
    "senna": 7,
    "abed": 6
}

preferences = {
    "bob": {
        "Mon": ["morn", "aft"],
        "Tue": [],
        "Wed": ["eve"],
        "Thu": [],
        "Fri": []
    },
    "senna": {
        "Mon": [],
        "Tue": ["eve"],
        "Wed": [],
        "Thu": [],
        "Fri": ["morn"]
    },
    "abed": {
        "Mon": ["morn"],
        "Tue": ["morn"],
        "Wed": ["eve"],
        "Thu": [],
        "Fri": ["morn"]
    }
}

headcounts = {
    "Mon": {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    "Tue": {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    "Wed": {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    "Thu": {
        8: 1,
        9: 1,
        10: 1,
        11: 1
    },
    "Fri": {
        8: 1,
        9: 1,
        10: 1,
        11: 0
    }
}

# intervals per day and hour (M - F vertical and then 8-12PM horizontal)
intervals = {
    "Mon": {
        8: ["senna"],
        9: ["random"],
        10: ["abed"],
        11: ["random"]
    },
    "Tue": {
        8: ["bob"],
        9: ["bob"],
        10: ["bob"],
        11: ["random"]
    },
    "Wed": {
        8: ["senna"],
        9: ["bob"],
        10: ["random"],
        11: ["random"]
    },
    "Thu": {
        8: ["random"],
        9: ["bob"],
        10: ["bob"],
        11: ["bob"]
    },
    "Fri": {
        8: ["senna"],
        9: ["abed"],
        10: ["random"],
        11: []
    }
}

OLD REQUIREMENTS BASED ON PRIOR INPUT DATA

def meets_requirements():

    ##########################################################################
    # vacation check
    for name, days_off in vacations.items():
        for day in days_off:
            actual_name_of_day_that_we_need = day.split(" ")[0]
            # print("{} should be off on {}".format(name, actual_name_of_day_that_we_need))
            # need to check that intervals[actual_name_of_day_that_we_need] must not contain name

            # intervals[actual_name_of_day_that_we_need].values() gives a list of people scheduled at every hour of that day
            for scheduled_people_in_a_certain_hour in intervals[actual_name_of_day_that_we_need].values():
                if name in scheduled_people_in_a_certain_hour:
                    print("{} got scheduled on {}, but it's a vacation".format(name, actual_name_of_day_that_we_need))
                    return False

    ##########################################################################
    # required hours check
    for name,number_of_hours_required in required.items():
        number_of_times_name_pops_up = 0
        for day, hours in intervals.items():
            for hour, scheduled_people in hours.items():

                if name in scheduled_people:
                    number_of_times_name_pops_up += 1
        print(number_of_times_name_pops_up) # printing 7 right now for bob, 3 for senna, and N/A for abed (?)
        # at this point, number of times name pops up is the right amount
        if number_of_times_name_pops_up < number_of_hours_required:
            print("{} popped up {} time(s) but requires {}".format(name,number_of_times_name_pops_up, number_of_hours_required))
            return False
    return True



def head_count_requirements():

    ##########################################################################
    # head count is filled, no more no less
    # count number of people in each interval. if count =/= headcount then return an error

    for day, hours in headcounts.items():
        for hour, required_hours in hours.items():
            head_count_hours = 0
            head_count_hours += required_hours
            #print(head_count_hours)                # testing how many head_counts

    for day, hours in intervals.items():
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
    # if scheduled after vacation or evening shift, don't schedule morning shift
    # still figuring this out. can probably merge this with def meet_criteria
    # remove day of the week and replace with date

    for name, days_off in vacations.items():
        for day in days_off:
            actual_name_of_day_that_we_need = day.split(" ")[0] # monday
            # monday is a string right now, but we want to find the next date down the list. In other words, we want to call the next key)
            actual_name_of_day_that_we_need
            print(actual_name_of_day_that_we_need)



        for scheduled_people_in_a_certain_hour in intervals[actual_name_of_day_that_we_need].values():
            if name in scheduled_people_in_a_certain_hour:
                print("{} got scheduled on {}, but it's a vacation".format(name, actual_name_of_day_that_we_need))
                return False
            if name in

    return True


'''

d = OrderedDict([('aaaa', 'a',), ('bbbb', 'b'), ('cccc', 'c'), ('dddd', 'd'), ('eeee', 'e'), ('ffff', 'f')])
i = 'eeee'
link_prev, link_next, key = d._OrderedDict__map['eeee']
print ('nextKey: ', link_next[2], 'prevKey: ', link_prev[2])
'''



print("sum of available hours: {}".format(sumOfHoursAvailable()))
print("  total required hours: {}".format(numberOfHoursNeeded()))
#print("meets requirements? {}".format(meets_requirements()))
#print(pd.DataFrame.from_dict(intervals))
#print(head_count_requirements())
print(vacay_evening_check())



"""


