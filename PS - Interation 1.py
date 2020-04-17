from __future__ import print_function
from ortools.sat.python import cp_model
import numpy as np



'''
NEXT STEPS:
[x] 1. Need to reformat further the shift_requests. remove 'array' and replace with [].  
[x] 2. For now, concatenate all the groups to see if the program runs. I don't think you need to tweak anything
[ ] 3. Do we need to update the matrix so we can change number of shifts? Or is there a way for us to update min_num_shifts? 
[ ] 4. Once the above works, start to section out into groups (maybe use a dictionary??) 

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


def main():

#########################################################################################################

## CREATING GROUPS
# [total_EEs_in_group, days_required]

    group_1 = [3, 2]              # 2 full days
    group_2 = [2, 2]              # 1 full day and 2 half days
    # group_3    = [3, 2]            # 2 half days
    # group_4 = [2, 2]            # 2 full days and 1 half day
    # group_5 = [2, 1]


    ## creating matrices - we can create a function later!
    # put the matrix in a list or a dictionary. it becomes group_matrix[i]
    # def create_matrix(i):
    #     group_i_matrix = []
    #     for x in range(group_i[0]):
    #         matrix = np.random.randint(0, 2, size=(5,2)) # 5 days and 2 types of shifts
    #         group_i_matrix.append(matrix)
    #     return
    #
    #     group_i_matrix = np.vstack(group_i_matrix)
    #     print(group_i_matrix)
    #
    # create_matrix(i = 1)

    group_1_matrix = []
    for x in range(group_1[0]):
        matrix = np.random.randint(0, 2, size=(5, 2))       # 5 days and 2 shifts
        group_1_matrix.append(matrix)


    group_2_matrix = []
    for x in range(group_2[0]):
        matrix = np.random.randint(0, 2, size=(5, 2))
        group_2_matrix.append(matrix)

    # compile all the matrices
    compiled_matrix = list(np.concatenate((group_1_matrix,group_2_matrix)))


## CHECK - total hours for groupX meets hours required

    g1_stack = np.vstack((group_1_matrix))
    g2_stack = np.vstack((group_2_matrix))


    group_1_conversion = np.where(g1_stack == 0, 0.5, 1)
    group_2_conversion = np.where(g2_stack == 0, 0.5, 1)


    total_hours_group_1 = sum(sum(group_1_conversion))
    total_hours_group_2 = sum(sum(group_2_conversion))

    # days_req conditions
    days_required_group_1 = group_1[0] * group_1[1]
    days_required_group_2 = group_2[0] * group_2[1]

    if total_hours_group_1 < days_required_group_1:
        print("error")
    else:
        print('true')

    if total_hours_group_2 < days_required_group_2:
        print("error")
    else:
        print('true')


## DECLARING OTHER VARIABLES

    #num_nurses = group_1[0] + group_2[0]
    num_nurses = 5
    num_shifts = 8
    num_days = 5
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    #shift_requests = compiled_matrix
    shift_requests = [[[0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]],
                      [[1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0]],
                      [[0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]]


#########################################################################################################

## CREATE THE MODEL

    model = cp_model.CpModel()

    # Creates all shift variables and stores them in a list.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))


    # Each shift is assigned to exactly one nurse in .
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # min_shifts_assigned is the largest integer such that every nurse can be assigned at least that number of shifts.

    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)

    model.Maximize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses    # finding the sum of shift_request matrix
            for d in all_days for s in all_shifts))


## CREATE THE SOLVER

    solver = cp_model.CpSolver()
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for n in all_nurses:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:
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