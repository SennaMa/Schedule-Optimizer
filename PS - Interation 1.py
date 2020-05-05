from __future__ import print_function
from ortools.sat.python import cp_model
import numpy as np


# ## SAMPLE

# After speaking with Kiss, we should add the following fields:
# [ ] French vs English agent
# [ ] Available days



class Nurse():   # input agent details (ie. name, hours required, shift preference)

    def __init__(self,name,hours_required,shift_preference):
        self.name = name
        self.hours_required = hours_required
        self.shift_preference = shift_preference
        self.mon = [shift_preference[0]]
        self.tues = [shift_preference[1]]
        self.wed = [shift_preference[2]]
        self.thurs = [shift_preference[3]]
        self.fri = [shift_preference[4]]
        self.total_shift = [self.mon,self.tues,self.wed,self.thurs,self.fri]
    
    def set_shift(self, x):
        self.shift_preference = x
        self.total_shift = x
    
    # pulls the entire list of shift preferences
    def get_shift(self):
        print(self.total_shift)
        return self.total_shift

    # only pulls the requested shift preference as a numerical value
    def shift_interpreter_num(self,index1):
        print(self.total_shift[index1])


    # pulls the requested shift as a day
    def get_date(self,index1):
        print(self.total_shift[index1])
        if index1 == 0:
            print('Monday')
        elif index1 == 1:
            print('Tuesday')
        elif index1 == 2:
            print('Wednesday')
        elif index1 == 3:
            print('Thursday')
        elif index1 == 4:
            print('Friday')
        return self.total_shift[index1]
    
    # pulls the preference (full or half)
    def get_preference(self,index1):
        print(self.total_shift[index1])

        def full_or_half():
            if self.total_shift[index1] == [0, 1]:
                print("Half")
            elif self.total_shift[index1] == [1, 0]:
                print("Full")
            elif self.total_shift[index1] == [0, 0]:
                print("No booking")
        return full_or_half()

# # entering agents in class nurse(). we can build a function that populates this list
# nurse0 = Nurse("Senna",2,([[0,1],[0,0],[0,0],[0,0],[0,0]]))
#
# print(nurse0.shift_preference)
# print(nurse0.fri)                                         # prints schedule pref on Friday based on a string
# nurse0.shift_interpreter_num(4)                           # prints schedule pref on Friday based on an integer
#
# nurse0.set_shift([[0,1],[0,0],[0,0],[0,0],[0,1]])         # changes schedule pref for Nurse0
# nurse0.get_shift()                                        # retrieves and prints the new shift
#
# nurse0.get_date(4)                                        # retrieves the date you're looking for
# nurse0.get_preference(4)                                  # retrieve preference on Friday (works the half day)

'''

## In our example we're going to have five agents with different schedule preferences
# Declaring agents with random matrices

    nurse0 = Nurse("Senna",2,([[1,0],[0,0],[0,0],[0,1],[1,0]]))
    nurse1 = Nurse("Josh",2,([[0,0],[0,0],[0,0],[0,0],[0,0]]))
    nurse2 = Nurse("Nina",2,([[0,1],[1,0],[0,0],[1,0],[1,0]]))
    nurse3 = Nurse("Christine",2,([[1,0],[0,0],[0,0],[0,0],[0,1]]))
    nurse4 = Nurse("Niccoh",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))
    nurse5 = Nurse("Bob",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))
    nurse6 = Nurse("Bob1",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))
    nurse7 = Nurse("Bob2",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))
    nurse8 = Nurse("Bob3",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))
    nurse9 = Nurse("Bob4",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))


# checks to see if schedule requests meets hours_required per agent

    nurse0_num_of_requested_hours = 0
    for days in nurse0.shift_preference:
        if days == [0, 1] or days == [1,0]:
            nurse0_num_of_requested_hours += 1
        elif days == [0, 0]:
            nurse0_num_of_requested_hours += 0


    if nurse0_num_of_requested_hours < nurse0.hours_required:
        print("error")
    else:
        print('true')



## DECLARING OTHER VARIABLES

    num_nurses = 4
    num_shifts = 3
    num_days = 3
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    shift_requests = [[[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1],
                       [0, 1, 0], [0, 0, 1]],
                      [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
                       [0, 0, 0], [0, 0, 1]],
                      [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
                       [0, 1, 0], [0, 0, 0]],
                      [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
                       [1, 0, 0], [0, 0, 0]],
                      [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],
                       [0, 1, 0], [0, 0, 0]]]


## Next steps: update shift_requests so it interacts with our classes! Change number of nurses to 5 to make the program work. Also change num_shifts to 2
# on line 286 it's taking each shift_request (so 1 and then 0 in nurse0's monday shift) and multiplying it by (n, d, s). However
#   an error occurs because you're trying to multiple 2 values when it's expecting 8 (since there are 8 potential shifts)

# what's confusing is how there can be different number of shift preferences (ie. morning or afternoon), but more than one shift per day
## the error is coming from shifts[(n, d, s)]. It's expecting 8 variables (since there are 8 shifts) but only getting 2 preferences (I think)

                   [[[1, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [1, 0], [0, 0], [0, 0], [1, 0]],
                      [[0, 0], [1, 0], [1, 0], [0, 0], [0, 0]],
                      [[1, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [0, 0], [1, 0], [0, 0], [1, 0]],
                      [[0, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [1, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [1, 0], [0, 0]]]
'''



## Create a program that creates random matrices

# number of placeholders in half a set
morning_shifts = 6
evening_shifts = 6
num_of_agents_available = 11



# create day by day
y = ["Morning", "Morning", "Evening", "Evening", "Morning", "Not_available", "Evening", "Morning", "Evening", "Evening", "Evening"]
for x in range(num_of_agents_available):
    if y[x] != "Not_available":
        print(np.random.randint(2,size=morning_shifts))
    else: print("Not_Available")

## next steps: add commas to separate the values in the matrix. once complete, you can create the new schedule_pref which will comprise of [morning + evening]
## example: morning = [0,0,0,0,0,1,0,0,0,0,0,0] vs evening = [0,0,0,0,0,0,0,0,0,0,0,1]
## enter final matrix into program and iteration 1 is complete


'''

def main():
    num_nurses = 11
    num_shifts = 2
    num_days = 5
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    shift_requests = [[[1, 0], [0, 1], [0, 1], [0, 0], [0, 0]], [[1, 0], [1, 0], [0, 1], [0, 0], [1, 0]],
                     [[0, 1], [0, 1], [1, 0], [1, 0], [0, 1]], [[1, 0], [0, 0], [0, 1], [0, 1], [0, 1]],
                     [[0, 1], [0, 1], [0, 1], [1, 0], [1, 0]], [[0, 0], [0, 0], [0, 1], [1, 0], [1, 0]],
                     [[0, 1], [0, 1], [0, 1], [1, 0], [0, 1]], [[1, 0], [1, 0], [0, 0], [1, 0], [0, 1]],
                     [[1, 0], [0, 1], [0, 1], [0, 1], [1, 0]], [[0, 1], [1, 0], [0, 1], [0, 1], [0, 1]],
                     [[0, 1], [1, 0], [1, 0], [0, 1], [0, 1]]]


    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works on day 'd' for shift 's'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    print(shifts)

    # Each shift is assigned to exactly one nurse in .
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # min_shifts_assigned is the largest integer such that every nurse can be
    # assigned at least that number of shifts.
    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)

    model.Maximize(                                                     # finds the product between shift_req and actual shifts. if 1 then it will add on top of one another. In the end the program will find the solution with the largest sum
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses
            for d in all_days for s in all_shifts))
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for n in all_nurses:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:                # if shift for n,d,s is part of the solution that gen max values then you include it
                    if shift_requests[n][d][s] == 1:
                        print('Nurse', n, 'works shift', s, '(requested).')
                    else:
                        print('Nurse', n, 'works shift', s, '(not requested).')
        print()

    # Statistics.
    print()
    print('Statistics')
    print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
          '(out of', num_nurses * min_shifts_per_nurse, ')')
    print('  - wall time       : %f s' % solver.WallTime())


if __name__ == '__main__':
    main()

'''

