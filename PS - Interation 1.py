from __future__ import print_function
from ortools.sat.python import cp_model
import numpy as np

'''
NEXT STEPS:
[x] 1. Need to reformat further the shift_requests. remove 'array' and replace with [].  
[x] 2. For now, concatenate all the groups to see if the program runs. I don't think you need to tweak anything
[ ] 3. Convert groups into classes. this will make your code easier to interpret 
[ ] 4. Do we need to update the matrix so we can change number of shifts? Or is there a way for us to update min_num_shifts?


1. Decide how many hours are required by week. 
2. How many shifts per day then? 
3. How many agents are available?               <- once this gets complicated, we can determine how many hours are required per agent  
4. Assuming equally spread out, how many shifts per agent? 
    Minimum - (num of shifts * num of days) / num of agents available
    Maximum - Minimum + 1 shift
5. 
'''


# ## SAMPLE
# shift_requests = [[[0, 0, 1],
#                    [0, 0, 0],
#                    [0, 0, 0],
#                    [0, 0, 0],
#                    [0, 0, 1],
#                    [0, 1, 0],
#                    [0, 0, 1]],
#                   [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
#                    [0, 0, 0], [0, 0, 1]],
#                   [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
#                    [0, 1, 0], [0, 0, 0]],
#                   [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
#                    [1, 0, 0], [0, 0, 0]],
#                   [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],
#                    [0, 1, 0], [0, 0, 0]]]

# ## If group_1 = 3,2 and group_2 = 5,2 and number of shift = 2
# shift_requests = [[[0, 1, 0], [0, 1, 1],[0, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0]],
#                       [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 0]],
#                       [[1, 1, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0]],
#                       [[0, 0, 0], [1, 1, 0], [0, 1, 1], [0, 0, 0], [0, 1, 1]],
#                       [[0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
#                       [[0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 1, 0]],
#                       [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]],
#                       [[1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]]

# shift_requests = [
#     [[0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 0, 0]],
#     [[0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 0, 0]],
#     [[1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 0, 0]],
#     [[0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 1, 1, 0, 0, 0, 0, 0]],
#     [[0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0]],
#     [[0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0, 0, 0, 0]],
#     [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0],
#      [0, 0, 0, 0, 0, 0, 0, 0]],
#     [[1, 0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
#      [0, 0, 1, 0, 0, 0, 0, 0]]]

# incorporating classes

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


def main():

# PUTTING THE IDEA OF GROUPS ON PAUSE. May revisit later
    # group_1 = [3, 2]  # 2 full days
    # group_2 = [2, 2]  # 1 full day and 2 half days
    # # group_3    = [3, 2]            # 2 half days
    # # group_4 = [2, 2]            # 2 full days and 1 half day
    # # group_5 = [2, 1]
    #
    #
    # group_1_matrix = []
    #
    # for x in range(group_1[0]):
    #     matrix = np.random.randint(0, 2, size=(5, 2))
    #     group_1_matrix.append(matrix)
    #
    # group_1_matrix = np.vstack(group_1_matrix)
    # #print(group_1_matrix)
    #
    # group_2_matrix = []
    #
    # for x in range(group_2[0]):
    #     matrix = np.random.randint(0, 2, size=(5, 2))
    #     group_2_matrix.append(matrix)
    #
    # group_2_matrix = np.vstack(group_2_matrix)
    # # print(group_2_matrix)

    ## declaring constraints - can make this into a function as well

    # group_1_conversion = np.where(group_1_matrix < 1, 0.5, 1)
    # group_2_conversion = np.where(group_2_matrix < 1, 0.5, 1)
    #
    # total_hours_group_1 = sum(sum(group_1_conversion))
    # total_hours_group_2 = sum(sum(group_2_conversion))
    #
    # # print(group_1_conversion)
    # # print(total_hours_group_1)
    #
    # # days_req conditions
    # days_required_group_1 = group_1[0] * group_1[1]
    # days_required_group_2 = group_2[0] * group_2[1]
    #
    # if total_hours_group_1 < days_required_group_1:
    #     print("error")
    # else:
    #     print('true')
    #
    # if total_hours_group_2 < days_required_group_2:
    #     print("error")
    # else:
    #     print('true')


## In our example we're going to have five agents with different schedule preferences
# Declaring agents with random matrices

    nurse0 = Nurse("Senna",2,([[0,1],[0,0],[0,0],[0,0],[0,0]]))
    nurse1 = Nurse("Josh",2,([[0,0],[0,0],[0,0],[0,0],[0,0]]))
    nurse2 = Nurse("Nina",2,([[0,1],[1,0],[0,0],[1,0],[1,0]]))
    nurse3 = Nurse("Christine",2,([[1,0],[0,0],[0,0],[0,0],[0,1]]))
    nurse4 = Nurse("Niccoh",2,([[0,1],[0,1],[0,1],[0,1],[0,0]]))


## next steps: work on getting the check to work. it looks like TypeError: '<' not supported between instances of 'list' and 'int'
# checks to see if list = hours_required



    print(nurse0.shift_preference)
    group_1_conversion = np.where(nurse0.shift_preference < 1, 0.5, 1)
    total_hours_group_1 = sum(sum(group_1_conversion))

    print(group_1_conversion)
    print(total_hours_group_1)

    # days_req conditions
    days_required_group_1 = nurse0.hours_required

    if total_hours_group_1 < days_required_group_1:
        print("error")
    else:
        print('true')

    #
    # # compile all the matrices
    # schedule_preference = np.concatenate((group_1_matrix,group_2_matrix)) # not correct - it needs to split and look like this (see below)
    # #print(schedule_preference)
    #
    #
    # ## DECLARING OTHER VARIABLES
    #
    # num_nurses = 5
    # num_shifts = 2
    # num_days = 5
    # all_nurses = range(num_nurses)
    # all_shifts = range(num_shifts)
    # all_days = range(num_days)
    # # shift_requests = compiled_matrix
    # shift_requests = [[[0, 1], [0, 1], [0, 0], [0, 1],
    #      [0, 1]],
    #     [[0, 0], [1, 0], [1, 0], [0, 0],
    #      [0, 1]],
    #     [[1, 0], [0, 1], [0, 0], [0, 0],
    #      [0, 1]],
    #     [[0, 0], [1, 0], [0, 1], [0, 0],
    #      [0, 1]],
    #     [[0, 1], [0, 1], [0, 0], [0, 0],
    #      [0, 0]]]


#
# # Creates the model.
#     model = cp_model.CpModel()
#
#     # Creates shift variables.
#     # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
#     shifts = {}
#     for n in all_nurses:
#         for d in all_days:
#             for s in all_shifts:
#                 shifts[(n, d,
#                         s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
#
#     # Each shift is assigned to exactly one nurse in .
#     for d in all_days:
#         for s in all_shifts:
#             model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)
#
#     # Each nurse works at most one shift per day.
#     for n in all_nurses:
#         for d in all_days:
#             model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)
#
#     # min_shifts_assigned is the largest integer such that every nurse can be
#     # assigned at least that number of shifts.
#     min_shifts_per_nurse = 3
#     max_shifts_per_nurse = min_shifts_per_nurse + 1
#     for n in all_nurses:
#         num_shifts_worked = sum(
#             shifts[(n, d, s)] for d in all_days for s in all_shifts)
#         model.Add(min_shifts_per_nurse <= num_shifts_worked)
#         model.Add(num_shifts_worked <= max_shifts_per_nurse)
#
#     model.Maximize(                                                                         # finds the product between shift_req and actual shifts. if 1 then it will add on top of one another. In the end the program will find the solution with the largest sum
#         sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses
#             for d in all_days for s in all_shifts))
#     # Creates the solver and solve.
#     solver = cp_model.CpSolver()
#     solver.Solve(model)
#     for d in all_days:
#         print('Day', d)
#         for n in all_nurses:
#             for s in all_shifts:
#                 if solver.Value(shifts[(n, d, s)]) == 1:                        # if shift for n,d,s is part of the solution that gen max values then you include it
#                     if shift_requests[n][d][s] == 1:
#                         print('Nurse', n, 'works shift', s, '(requested).')
#                     else:
#                         print('Nurse', n, 'works shift', s, '(not requested).')
#         print()
#
#     # Statistics.
#     print()
#     print('Statistics')
#     print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
#           '(out of', num_nurses * min_shifts_per_nurse, ')')
#     print('  - wall time       : %f s' % solver.WallTime())
#
#
if __name__ == '__main__':
    main()
