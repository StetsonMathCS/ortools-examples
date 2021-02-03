# https://app.codility.com/programmers/task/sheep_and_sunshades/

from ortools.sat.python import cp_model
import random

#xypairs = set()
#xs = []
#ys = []
#for i in range(100):
#    for j in range(100):
#        pair = (random.randint(1,100000), random.randint(1,100000))
#        if pair not in xypairs:
#            xypairs.add(pair)
#            xs.append(pair[0])
#            ys.append(pair[1])

xs = [0, 0, 10, 10]
ys = [0, 10, 0, 10]

model = cp_model.CpModel()

d = model.NewIntVar(0, 100000, "d")
twice_d = model.NewIntVar(0, 200000, "2*d")
model.Add(twice_d == 2*d)

width_intervals = []
height_intervals = []
for i in range(len(xs)):
    left = model.NewIntVar(-100000, 100000, "left")
    model.Add(left == xs[i] - d)
    right = model.NewIntVar(-100000, 100000, "right")
    model.Add(right == xs[i] + d)
    width_iv = model.NewIntervalVar(left, twice_d, right, "width_iv for shade %d" % i)
    width_intervals.append(width_iv)

    top = model.NewIntVar(-100000, 100000, "top")
    model.Add(top == ys[i] + d)
    bottom = model.NewIntVar(-100000, 100000, "bottom")
    model.Add(bottom == ys[i] - d)
    height_iv = model.NewIntervalVar(bottom, twice_d, top, "height_iv for shade %d" % i)
    height_intervals.append(height_iv)

model.AddNoOverlap2D(width_intervals, height_intervals)

model.Maximize(d)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("D = %d" % solver.Value(d))


