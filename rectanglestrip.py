# https://app.codility.com/programmers/task/rectangles_strip/

from ortools.sat.python import cp_model
import random

#A = []
#B = []
#for i in range(10000):
#    A.append(random.randint(1,1000000))
#for i in range(10000):
#    B.append(random.randint(1,1000000))

A = [2, 10, 4, 1, 4]
B = [4, 1, 2, 2, 5]

model = cp_model.CpModel()

strip_height = model.NewIntVar(1, 1000000000, "strip height")

in_strip_vars = []
rotated_in_strip_vars = []
for i in range(len(A)):
    in_strip_vars.append(model.NewBoolVar("rectangle %d in strip" % i))
    rotated_in_strip_vars.append(model.NewBoolVar("rectangle %d rotated in strip" % i))
    model.Add(A[i] == strip_height).OnlyEnforceIf(in_strip_vars[i])
    model.Add(B[i] == strip_height).OnlyEnforceIf(rotated_in_strip_vars[i])

model.Maximize(sum(in_strip_vars + rotated_in_strip_vars)) # count number of true bools

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    for i in range(len(A)):
        if solver.Value(in_strip_vars[i]):
            print("In strip: %d x %d" % (B[i], A[i]))
        elif solver.Value(rotated_in_strip_vars[i]):
            print("In strip rotated: %d x %d" % (A[i], B[i]))


